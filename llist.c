#include"llist.h"
// Insert at the beginning of the list
list* insert(list *head)
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
// Delete node from the left
list* deleteAtLeft(list *head) 
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
// Delete the First node 
list* deleteFirst(list *head) 
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
// Search for a value in the linked list
void search(list *head , int key) 
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
// Display the linked list
void display(list *head) 
{
    if (head == NULL) {
        printf("Linked List is Empty\n");
        return;
    }

    while (head != NULL) {
        printf("%d  ", head->data);
        head = head->next;
    }
    printf("\n");
}
// Count the number of nodes in the linked list
int count(list *head) 
{
    int c = 0;
    while (head != NULL) {
        c++;
        head = head->next;
    }
    return c ;
}
// Reverse display using recursion
void Rdisplay(list *head) 
{
    if (head != NULL) {
        int temp = head->data;
        Rdisplay(head->next);
        printf("%d  ", temp);
    }
}
