import json
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .queries import QUERY_CHOICES


@staff_member_required
@require_GET
def query_builder(request):
    """Admin page: choose one of 10 preset queries and run it."""
    queries_json = json.dumps([[q[0], q[1], q[2]] for q in QUERY_CHOICES])
    return render(request, 'reports/query_builder.html', {
        'queries': QUERY_CHOICES,
        'queries_json': queries_json,
    })


@staff_member_required
@require_POST
def query_builder_run(request):
    """Run selected query with params and return HTML table (for display and print)."""
    query_key = request.POST.get('query_key')
    if not query_key:
        return render(request, 'reports/query_result.html', {'rows': [], 'error': 'No query selected'})
    chosen = next((q for q in QUERY_CHOICES if q[0] == query_key), None)
    if not chosen:
        return render(request, 'reports/query_result.html', {'rows': [], 'error': 'Unknown query'})
    _, _, param_names, run_func = chosen
    params = {}
    for p in param_names:
        val = request.POST.get(p)
        if val is not None and val != '':
            if p in ('limit', 'town_id', 'region_id'):
                try:
                    params[p] = int(val)
                except ValueError:
                    pass
            elif p in ('price_min', 'price_max'):
                try:
                    params[p] = float(val)
                except ValueError:
                    pass
            else:
                params[p] = val
    try:
        rows = run_func(**params)
    except Exception as e:
        return render(request, 'reports/query_result.html', {'rows': [], 'error': str(e), 'post_params': {}})
    if not rows:
        return render(request, 'reports/query_result.html', {
            'rows': [], 'columns': [], 'query_label': chosen[1],
            'post_params': {k: request.POST.get(k) for k in ['query_key'] + param_names},
        })
    columns = list(rows[0].keys()) if rows else []
    # For template: list of lists (each row = list of values in column order)
    rows_vals = [[r.get(col, '') for col in columns] for r in rows]
    # Keep POST data for export form
    post_params = {'query_key': query_key}
    for p in param_names:
        v = request.POST.get(p)
        if v is not None:
            post_params[p] = v
    return render(request, 'reports/query_result.html', {
        'rows': rows_vals,
        'columns': columns,
        'query_label': chosen[1],
        'post_params': post_params,
    })


@staff_member_required
@require_POST
def query_export_excel(request):
    """Re-run the same query and return .xlsx file."""
    query_key = request.POST.get('query_key')
    if not query_key:
        return HttpResponse('No query selected', status=400)
    chosen = next((q for q in QUERY_CHOICES if q[0] == query_key), None)
    if not chosen:
        return HttpResponse('Unknown query', status=400)
    _, _, param_names, run_func = chosen
    params = {}
    for p in param_names:
        val = request.POST.get(p)
        if val is not None and val != '':
            if p in ('limit', 'town_id', 'region_id'):
                try:
                    params[p] = int(val)
                except ValueError:
                    pass
            elif p in ('price_min', 'price_max'):
                try:
                    params[p] = float(val)
                except ValueError:
                    pass
    try:
        rows = run_func(**params)
    except Exception as e:
        return HttpResponse(str(e), status=500)
    columns = list(rows[0].keys()) if rows else []
    try:
        import openpyxl
        from io import BytesIO
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Query result"
        ws.append(columns)
        for r in rows:
            ws.append([r.get(c, '') for c in columns])
        buf = BytesIO()
        wb.save(buf)
        buf.seek(0)
        resp = HttpResponse(buf.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        resp['Content-Disposition'] = 'attachment; filename=query_result.xlsx'
        return resp
    except ImportError:
        import csv
        from io import StringIO
        buf = StringIO()
        w = csv.writer(buf)
        w.writerow(columns)
        for r in rows:
            w.writerow([r.get(c, '') for c in columns])
        resp = HttpResponse(buf.getvalue(), content_type='text/csv; charset=utf-8')
        resp['Content-Disposition'] = 'attachment; filename=query_result.csv'
        return resp
