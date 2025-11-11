#ifndef DSHELP_H
#define DSHELP_H
//INCLUDES (Consolidated from all headers)
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <limits.h>
//LINKED LIST (from llist.h)
typedef struct Linked_List
{
    int data ;
    struct Linked_List *next ;
} list;
list* llist_insert(list *head);
list* llist_deleteAtLeft(list *head);
list* llist_deleteLast(list *head);
void  llist_display(list *head);
int   llist_count(list *head);
void  llist_search(list *head , int key);
void  llist_Rdisplay(list *head);
//BINARY SEARCH TREE (from bst.h)
typedef struct Binary_Search_Tree
{
    struct Binary_Search_Tree *left;
    int data;
    struct Binary_Search_Tree *right;
} tree;
tree* bst_insert(tree* root, int x);
void  bst_displayPostorder(tree* root);
void  bst_displayPreorder(tree* root);
void  bst_displayInorder(tree* root);
int   bst_countNodes(tree* root, int c);
int   bst_One_child(tree* root, int c);
int   bst_Two_child(tree* root, int c);
int   bst_Common_Parent(tree* root, int c);
tree* bst_Delete_Node(tree* root, int key);
// GRAPH (from graph.h)
/*Node structure for adjacency list representation*/
typedef struct Node {
    int vertex;           // Destination vertex
    int weight;          // Weight of the edge (for weighted graphs)
    struct Node* next;   // Pointer to next node in the list
} Node;
/*Graph structure using adjacency list representation*/
typedef struct Graph {
    int numVertices;     // Total number of vertices in the graph
    Node** adjLists;     // Array of adjacency lists
    bool* visited;       // Array to track visited vertices (for traversals)
} Graph;
/*Queue structure for BFS implementation*/
typedef struct Queue {
    int* items;          // Array to store queue elements
    int front;           // Front index
    int rear;            // Rear index
    int capacity;        // Maximum capacity of the queue
} Queue;
/*CORE GRAPH FUNCTIONS*/
Graph* createGraph(int vertices);
void   addEdge(Graph* graph, int src, int dest, int weight);
void   removeEdge(Graph* graph, int src, int dest);
void   displayGraph(Graph* graph);
void   freeGraph(Graph* graph);
/*GRAPH TRAVERSAL ALGORITHMS*/
void bfs(Graph* graph, int startVertex);
void dfs(Graph* graph, int startVertex);
void dfsUtil(Graph* graph, int vertex);
/*SHORTEST PATH ALGORITHMS*/
void dijkstra(Graph* graph, int startVertex);
/*GRAPH UTILITY FUNCTIONS*/
Node* createNode(int vertex, int weight);
Queue* createQueue(int capacity);
bool   isEmpty(Queue* queue);
bool   isFull(Queue* queue);
void   enqueue(Queue* queue, int item);
int    dequeue(Queue* queue);
void   freeQueue(Queue* queue);
int    minDistance(int dist[], bool visited[], int vertices);
#endif