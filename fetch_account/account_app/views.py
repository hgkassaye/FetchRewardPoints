from django.shortcuts import render, redirect
from django.db.models import Sum
from datetime import date, datetime
from .models import TransactionList, AggregatePointList, RedemedPointSummary
from .forms import NewTransactionForm

"""
renders home page 
"""
def index(request):

    return render(request, 'home.html')

""" 
view called for the addtransaction/ path 
this view will make updates two both TransactionList and AggregatePointList models.
check to see if there is an entry for the payer name on the same date as the transaction date 
of the new record. If there is a match, update points available for the payer. 
If a matching record does not exist, add a new record
"""
def addTransaction(request):

    if (request.method == "POST"):
        form = NewTransactionForm(request.POST)
        #make sure form is valid (add custome validation in the future)
        if form.is_valid():
            form.save(commit = False)
            # convert payee name to all caps to make comparission easier; extract information from the form to use to aggregate avilable points. 
            payerName = form['payerName'].value().upper()
            transactionDate = datetime.strptime(form['transactionDate'].value(), '%m/%d/%Y').isoformat()
            pointAmount = form['availablePoints'].value()
            #commit changes to the model
            form.save()

            # if the AggregatePointList table is empty, save the first entry 
            if (len(AggregatePointList.objects.all()) == 0):
                newAggPointRecord = AggregatePointList()
                newAggPointRecord.payerName = payerName
                newAggPointRecord.availablePoints = pointAmount
                newAggPointRecord.transactionDate = transactionDate
                newAggPointRecord.save()
            else:
                # check that we have entry for the payer on the same date
                if (AggregatePointList.objects.filter(payerName = payerName).filter(transactionDate = transactionDate).exists()):
                    #get the object to modify
                    obj =  AggregatePointList.objects.filter(payerName = payerName).filter(transactionDate = transactionDate).values()
                    #retrive a record from table with the id that matches the filter
                    retrieveRecord = AggregatePointList.objects.get(id = obj[0]['id'])
                    retrieveRecord.availablePoints = int(retrieveRecord.availablePoints) + int(pointAmount)
                    retrieveRecord.save()
                    
                #if either the payer or a record for the payer on that date does not exist, add a new record
                else:
                    newAggPointRecord = AggregatePointList()
                    newAggPointRecord.payerName = payerName
                    newAggPointRecord.availablePoints = pointAmount
                    newAggPointRecord.transactionDate = transactionDate
                    newAggPointRecord.save()

            return redirect('agg_report')

    # if a GET request, return the model form to render
    else:
        form = NewTransactionForm()

    return render(request, 'add_transaction.html', context={'form':form})

"""
view rendered when a user wants to spend their points
check that the user has enough points to redeem what they requested
if they have enought available points, the AggregatePointList table is updated 
to take into accoun the points redeemed with oldeest points redeemed first.
If all points of a record are redeemed, the record will be deleted from the table.
"""
def spendPoints(request):

    # delete all records of previous points transacted before processing a new spend request
    obj = RedemedPointSummary.objects.all()
    obj.delete()

    if (request.method == 'POST'):

        # extract the value from the post request and cast to an integer value
        requestedPoints = int(request.POST['pointsToUse'])

        #calculate total available points to use and check user is not requesting more than available
        totalAvailableBalance = AggregatePointList.objects.all().aggregate(Sum('availablePoints'))['availablePoints__sum']
        if (requestedPoints > totalAvailableBalance):
            return redirect('redemed_points')
            
        else:
            # use up available points to redeem until requestedPoints = 0
            while (requestedPoints > 0):
                # order point list from oldest to latest and get the first record
                obj = AggregatePointList.objects.order_by('transactionDate', 'availablePoints').first()

                # check if first record retrived has enough points to meet the requested points
                if (int(obj.availablePoints) >= requestedPoints):
                    pointsRecord = AggregatePointList.objects.get(id = obj.id)
                    remainingBalance = pointsRecord.availablePoints - requestedPoints
                    if (remainingBalance > 0):
                        # update the record to account for redeemed points
                        pointsRecord.availablePoints = remainingBalance
                        pointsRecord.save()
                    else:
                        # if the available balance after redeeming is 0, delete the record from the table.
                        pointsRecord.delete()
                    
                    # create records of payer's balance used to redeem requested points
                    redemedPayerDetails = RedemedPointSummary()
                    redemedPayerDetails.payerName = obj.payerName
                    redemedPayerDetails.availablePoints = requestedPoints
                    redemedPayerDetails.save()

                    # set requestedPoints to 0 sicne the user is able to redeeam it all
                    requestedPoints = 0

                # if points requested is more than the oldest record retrieved
                else:
                    # update the RedemedPointSummary table
                    redemedPoints = RedemedPointSummary()
                    redemedPoints.payerName = obj.payerName
                    redemedPoints.availablePoints = obj.availablePoints
                    redemedPoints.save()

                    # calculate requested points remaining to stil redeem
                    requestedPoints = requestedPoints - int(obj.availablePoints)
                    # delete the record since all points have been redeemed
                    pointsRecord = AggregatePointList.objects.get(id = obj.id)
                    pointsRecord.delete()
                
            return redirect('redemed_points')     

    return render(request, 'transact_point.html')

"""
view called for the points/detail path. 
This view renders the full transction list. This view should only maybe availbale for
an admin. Once user authentication is implemented, check loged user is a super_user
to view.
"""
def pointsReport(request):
    pointList = TransactionList.objects.all()
    return render(request, 'point_detail.html', context = {'point_lists':pointList})
"""
view called when points/agg path is called when a user 
wants to see a detailed list of available points
"""
def pointsAggReport(request):
    pointList = AggregatePointList.objects.all()
    return render(request, 'agg_point_detail.html', context = {'point_lists':pointList})

"""
view rendered when the path points/balance called
returns total available reward points to render  
"""
def totalBalance(request):
    totalBalance = AggregatePointList.objects.all().aggregate(Sum('availablePoints'))['availablePoints__sum']
    return render(request, 'point_balance.html', context = {'total_balance':totalBalance})

"""
view rendered on a successful call to redeem reward points
"""
def redemedPoints(request):
    redemedPoints = RedemedPointSummary.objects.all()
    return render(request, 'used_point_confirmation.html', context={'redemed_points':redemedPoints})