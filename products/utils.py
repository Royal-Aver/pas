from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline

from products.models import Product


def q_search(query):
    # if query.isdigit() and len(query) <= 7:
    #     return Product.objects.filter(id=int(query))

    # keywords = [word for word in query.split() if len(word) > 2]

    # q_objects = Q()

    # for keyword in keywords:
    #     q_objects |= Q(description__icontains=keyword)
    #     q_objects |= Q(title__icontains=keyword)

    # return Product.objects.filter(q_objects)

    vector = SearchVector('title', 'description')
    query_obj = SearchQuery(query)

    query_res = Product.objects.annotate(
        rank=SearchRank(vector, query_obj)).filter(
            rank__gt=0).order_by('-rank')

    query_res = query_res.annotate(
        headline=SearchHeadline(
            "title",
            query,
            start_sel='<span style="background-color: yellow">',
            stop_sel="</span>",
        )
    )

    query_res = query_res.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )

    return query_res
