#ifndef LLIST_H
#define LLIST_H

#include<stdio.h>
#include<stdlib.h>
typedef struct Linked_List
{
    int data ;
    struct Linked_List *next ;
}list;
//Functions Declaration
list* insert(list *head);
list* deleteAtLeft(list *head);
list* deleteFirst(list *head);
void display(list *head);
int count(list *head);
void search(list *head , int key);
void Rdisplay(list *head);

#endif
