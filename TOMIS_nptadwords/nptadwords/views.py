from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from .serializers import AccountSerializers


@api_view(['GET', 'UPDATE', 'DELETE'])
def get_delete_update_account(request, pk):
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of single account
    if request.method == 'GET':
        serializer = AccountSerializers(account)
        return Response(serializer.data)
    # delete single account
    elif request.method == 'DELETE':
        return Response({})
    # update detail of single account
    elif request.method == 'PUT':
        return Response({})


@api_view(['GET', 'POST'])
def get_post_accounts(request):
    # get all accounts
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializers(accounts, many=True)
        return Response(serializer.data)
    # insert a new record for an account
    elif request.method == 'POST':
        return Response({})
