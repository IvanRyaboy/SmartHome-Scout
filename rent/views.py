from django_filters.views import FilterView
from .models import Rent
from django.views.generic import DetailView


# class ApartmentsHomeView(FilterView):
#     template_name = "rent/rent_list.html"
#     model = Rent
#     paginate_by = 10
#     filterset_class = RentFilter


class ApartmentDetailView(DetailView):
    model = Rent
    context_object_name = 'rent'
    template_name = 'rent/rent_view.html'
