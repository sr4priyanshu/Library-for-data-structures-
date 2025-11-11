#include "dshelp.h" // Changed from llist.h
list* llist_insert(list *head)
{
    int x;
    printf("Enter the Value to be Inserted: ");
    scanf("%d", &x);
    
    list* ptr = (list*)malloc(sizeof(list));
    if (ptr != NULL) 
    {
        ptr->data = x;
        ptr->next = head;
        head = ptr;
    } else {
        printf("Node Creation Failed\n");
    }
    return head;
}
list* llist_deleteAtLeft(list *head) 
{
    if (head == NULL) 
    {
        printf("Linked List is Empty\n");
        return head;
    }

    list* ptr = head;
    int x = ptr->data;
    head = ptr->next;
    free(ptr);

    printf("Value %d has been Deleted\n", x);
    return head;
}
list* llist_deleteLast(list *head) 
{
    if (head == NULL) 
    {
        printf("Linked List is Empty\n");
        return head;
    }
    if (head->next == NULL) 
    {
        printf("Value %d has been Deleted\n", head->data);
        free(head);
        return NULL;
    }
    list* ptr1 = head;
    list* ptr2 = head->next;
    while (ptr2->next != NULL) 
    {
        ptr1 = ptr2;
        ptr2 = ptr2->next;
    }
    printf("Value %d has been Deleted\n", ptr2->data);
    free(ptr2);
    ptr1->next = NULL;
    return head;
}
void llist_search(list *head , int key) 
{
    int found = 0;

    while (head != NULL) 
    {
        if (head->data == key) 
        {
            found = 1;
            break;
        }
        head = head->next;
    }

    if (found)
        printf("Value Successfully Found\n");
    else
        printf("Value NOT Found\n");
}
void llist_display(list *head) 
{
    if (head == NULL) {
        printf("Linked List is Empty\n");
        return;
    }

    while (head != NULL) {
        printf("%d\n", head->data);
        head = head->next;
    }
    printf("\n");
}
int llist_count(list *head) 
{
    int c = 0;
    while (head != NULL) {
        c++;
        head = head->next;
    }
    return c ;
}
void llist_Rdisplay(list *head) 
{
    if (head != NULL) {
        int temp = head->data;
        llist_Rdisplay(head->next);
        printf("%d  ", temp);
    }
    printf("\n");
}