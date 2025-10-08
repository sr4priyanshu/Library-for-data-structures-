#include "llist.h"
int main() 
{
    list *head = NULL;
    int ch; int key ;

    do 
    {
        printf("Enter you Choice :\nPress 1 for Insertion\nPress 2 for Deletion from Left\nPress 3 for Deletion of First Node\nPress 4 for Display\nPress 5 to Search in Linked list\nPress 6 to Count the No. of Nodes\nPress 7 for Reverse Display\nPress 0 to EXIT.\t");
        scanf("%d",&ch);

        switch (ch) 
        {
            case 1:
                head = insert(head);
                break;
            case 2:
                head = deleteAtLeft(head);
                break;
            case 3:
                head = deleteFirst(head);
                break;
            case 4:
                display(head);
                break;
            case 5:
                printf("Input the Element to be Searched : ");
                scanf("%d",&key);
                search(head,key);
                break;
            case 6:
                count(head);
                break;
            case 7:
                if (head != NULL)
                    Rdisplay(head);
                else
                    printf("Linked List is Empty\n");
                break;
        }
    } while (ch != 0);

    return 0;
}