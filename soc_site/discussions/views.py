from django.shortcuts import render

def discussion_board(request):
    return render(request, 'discussions/board.html')