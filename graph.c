#include "dshelp.h" // Changed from graph.h
/* ====================
 * UTILITY FUNCTIONS
 * ==================== */
/**
 * Creates a new node for the adjacency list
 * Allocates memory and initializes the node with given vertex and weight
 */
Node* createNode(int vertex, int weight) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (!newNode) {
        printf("Error: Memory allocation failed for new node\n");
        return NULL;
    }
    newNode->vertex = vertex;
    newNode->weight = weight;
    newNode->next = NULL;
    return newNode;
}
/*
Creates a queue for BFS implementation
Initializes all queue properties and allocates memory for items array
*/
Queue* createQueue(int capacity) {
    Queue* queue = (Queue*)malloc(sizeof(Queue));
    if (!queue) {
        printf("Error: Memory allocation failed for queue\n");
        return NULL;
    }
    
    queue->items = (int*)malloc(capacity * sizeof(int));
    if (!queue->items) {
        printf("Error: Memory allocation failed for queue items\n");
        free(queue);
        return NULL;
    }
    
    queue->front = -1;
    queue->rear = -1;
    queue->capacity = capacity;
    return queue;
}

/**
 * Checks if the queue is empty
 * Queue is empty when front is -1 or front > rear
 */
bool isEmpty(Queue* queue) {
    return (queue->front == -1 || queue->front > queue->rear);
}

/**
 * Checks if the queue is full
 * Queue is full when rear reaches capacity - 1
 */
bool isFull(Queue* queue) {
    return (queue->rear == queue->capacity - 1);
}

/**
 * Adds an element to the rear of the queue
 * Handles the case when queue is initially empty
 */
void enqueue(Queue* queue, int item) {
    if (isFull(queue)) {
        printf("Queue is full\n");
        return;
    }
    
    if (queue->front == -1) {
        queue->front = 0;  // Initialize front when adding first element
    }
    queue->rear++;
    queue->items[queue->rear] = item;
}

/**
 * Removes and returns an element from the front of the queue
 * Returns -1 if queue is empty
 */
int dequeue(Queue* queue) {
    if (isEmpty(queue)) {
        printf("Queue is empty\n");
        return -1;
    }
    
    int item = queue->items[queue->front];
    queue->front++;
    
    // Reset queue when it becomes empty
    if (queue->front > queue->rear) {
        queue->front = queue->rear = -1;
    }
    
    return item;
}

/**
 * Frees memory allocated for the queue
 * Frees both the items array and the queue structure
 */
void freeQueue(Queue* queue) {
    if (queue) {
        free(queue->items);
        free(queue);
    }
}

/* ====================
 * CORE GRAPH FUNCTIONS
 * ==================== */

/**
 * Creates a new graph with the specified number of vertices
 * Initializes adjacency lists and visited array
 */
Graph* createGraph(int vertices) {
    // Validate input
    if (vertices <= 0) {
        printf("Error: Number of vertices must be positive\n");
        return NULL;
    }
    
    // Allocate memory for graph structure
    Graph* graph = (Graph*)malloc(sizeof(Graph));
    if (!graph) {
        printf("Error: Memory allocation failed for graph\n");
        return NULL;
    }
    
    graph->numVertices = vertices;
    
    // Allocate memory for adjacency lists array
    graph->adjLists = (Node**)malloc(vertices * sizeof(Node*));
    if (!graph->adjLists) {
        printf("Error: Memory allocation failed for adjacency lists\n");
        free(graph);
        return NULL;
    }
    
    // Allocate memory for visited array
    graph->visited = (bool*)malloc(vertices * sizeof(bool));
    if (!graph->visited) {
        printf("Error: Memory allocation failed for visited array\n");
        free(graph->adjLists);
        free(graph);
        return NULL;
    }
    
    // Initialize all adjacency lists as NULL and visited as false
    for (int i = 0; i < vertices; i++) {
        graph->adjLists[i] = NULL;
        graph->visited[i] = false;
    }
    
    printf("Graph created successfully with %d vertices\n", vertices);
    return graph;
}

/**
 * Adds an edge between source and destination vertices
 * Creates a directed edge from src to dest with given weight
 * For undirected graph, call this function twice (src->dest and dest->src)
 */
void addEdge(Graph* graph, int src, int dest, int weight) {
    // Validate input parameters
    if (!graph) {
        printf("Error: Graph is NULL\n");
        return;
    }
    
    if (src < 0 || src >= graph->numVertices || dest < 0 || dest >= graph->numVertices) {
        printf("Error: Invalid vertex numbers. Must be between 0 and %d\n", graph->numVertices - 1);
        return;
    }
    
    // Create new node for destination vertex
    Node* newNode = createNode(dest, weight);
    if (!newNode) {
        return;  // Error message already printed in createNode
    }
    
    // Add the new node at the beginning of the adjacency list
    newNode->next = graph->adjLists[src];
    graph->adjLists[src] = newNode;
    
    printf("Edge added: %d -> %d (weight: %d)\n", src, dest, weight);
}

/**
 * Removes an edge between source and destination vertices
 * Searches for the edge in the adjacency list and removes it
 */
void removeEdge(Graph* graph, int src, int dest) {
    // Validate input parameters
    if (!graph) {
        printf("Error: Graph is NULL\n");
        return;
    }
    
    if (src < 0 || src >= graph->numVertices || dest < 0 || dest >= graph->numVertices) {
        printf("Error: Invalid vertex numbers. Must be between 0 and %d\n", graph->numVertices - 1);
        return;
    }
    
    Node* current = graph->adjLists[src];
    Node* prev = NULL;
    
    // Search for the edge to remove
    while (current != NULL) {
        if (current->vertex == dest) {
            // Found the edge to remove
            if (prev == NULL) {
                // Removing the first node in the list
                graph->adjLists[src] = current->next;
            } else {
                // Removing a node in the middle or end
                prev->next = current->next;
            }
            free(current);
            printf("Edge removed: %d -> %d\n", src, dest);
            return;
        }
        prev = current;
        current = current->next;
    }
    
    printf("Edge not found: %d -> %d\n", src, dest);
}

/**
 * Displays the adjacency list representation of the graph
 * Shows all vertices and their connections with weights
 */
void displayGraph(Graph* graph) {
    if (!graph) {
        printf("Error: Graph is NULL\n");
        return;
    }
    
    printf("\n=== Graph Adjacency List ===\n");
    
    // Iterate through all vertices
    for (int v = 0; v < graph->numVertices; v++) {
        Node* temp = graph->adjLists[v];
        printf("Vertex %d: ", v);
        
        // Print all adjacent vertices
        if (temp == NULL) {
            printf("No connections");
        } else {
            while (temp) {
                printf("-> %d(w:%d) ", temp->vertex, temp->weight);
                temp = temp->next;
            }
        }
        printf("\n");
    }
    printf("=============================\n\n");
}

/**
 * Frees all memory allocated for the graph
 * Properly deallocates adjacency lists, visited array, and graph structure
 */
void freeGraph(Graph* graph) {
    if (!graph) {
        return;
    }
    
    // Free all nodes in adjacency lists
    for (int v = 0; v < graph->numVertices; v++) {
        Node* current = graph->adjLists[v];
        while (current) {
            Node* temp = current;
            current = current->next;
            free(temp);
        }
    }
    
    // Free the arrays and graph structure
    free(graph->adjLists);
    free(graph->visited);
    free(graph);
    
    printf("Graph memory freed successfully\n");
}

/* ========================
 * GRAPH TRAVERSAL ALGORITHMS
 * ======================== */

/**
 * Performs Breadth-First Search starting from a given vertex
 * Uses a queue to visit vertices level by level
 */
void bfs(Graph* graph, int startVertex) {
    // Validate input parameters
    if (!graph) {
        printf("Error: Graph is NULL\n");
        return;
    }
    
    if (startVertex < 0 || startVertex >= graph->numVertices) {
        printf("Error: Invalid start vertex. Must be between 0 and %d\n", graph->numVertices - 1);
        return;
    }
    
    // Reset visited array for fresh traversal
    for (int i = 0; i < graph->numVertices; i++) {
        graph->visited[i] = false;
    }
    
    // Create queue for BFS
    Queue* queue = createQueue(graph->numVertices);
    if (!queue) {
        return;
    }
    
    printf("\n=== BFS Traversal starting from vertex %d ===\n", startVertex);
    printf("Visit order: ");
    
    // Mark start vertex as visited and enqueue it
    graph->visited[startVertex] = true;
    enqueue(queue, startVertex);
    
    // Continue until queue is empty
    while (!isEmpty(queue)) {
        // Dequeue a vertex and print it
        int currentVertex = dequeue(queue);
        printf("%d ", currentVertex);
        
        // Get all adjacent vertices of the dequeued vertex
        Node* temp = graph->adjLists[currentVertex];
        while (temp) {
            int adjVertex = temp->vertex;
            
            // If adjacent vertex hasn't been visited, mark it and enqueue
            if (!graph->visited[adjVertex]) {
                graph->visited[adjVertex] = true;
                enqueue(queue, adjVertex);
            }
            temp = temp->next;
        }
    }
    
    printf("\n=======================================\n\n");
    freeQueue(queue);
}

/**
 * Helper function for recursive DFS implementation
 * Visits the current vertex and recursively visits all unvisited adjacent vertices
 */
void dfsUtil(Graph* graph, int vertex) {
    // Mark current vertex as visited and print it
    graph->visited[vertex] = true;
    printf("%d ", vertex);
    
    // Recursively visit all unvisited adjacent vertices
    Node* temp = graph->adjLists[vertex];
    while (temp) {
        int adjVertex = temp->vertex;
        if (!graph->visited[adjVertex]) {
            dfsUtil(graph, adjVertex);
        }
        temp = temp->next;
    }
}

/**
 * Performs Depth-First Search starting from a given vertex
 * Uses recursion to visit vertices in depth-first manner
 */
void dfs(Graph* graph, int startVertex) {
    // Validate input parameters
    if (!graph) {
        printf("Error: Graph is NULL\n");
        return;
    }
    
    if (startVertex < 0 || startVertex >= graph->numVertices) {
        printf("Error: Invalid start vertex. Must be between 0 and %d\n", graph->numVertices - 1);
        return;
    }
    
    // Reset visited array for fresh traversal
    for (int i = 0; i < graph->numVertices; i++) {
        graph->visited[i] = false;
    }
    
    printf("\n=== DFS Traversal starting from vertex %d ===\n", startVertex);
    printf("Visit order: ");
    
    // Start DFS from the given vertex
    dfsUtil(graph, startVertex);
    
    printf("\n=======================================\n\n");
}

/* ========================
 * SHORTEST PATH ALGORITHMS
 * ======================== */

/**
 * Finds the vertex with minimum distance value
 * Used by Dijkstra's algorithm to find the next vertex to process
 */
int minDistance(int dist[], bool visited[], int vertices) {
    int min = INT_MAX;
    int minIndex = -1;
    
    for (int v = 0; v < vertices; v++) {
        if (!visited[v] && dist[v] <= min) {
            min = dist[v];
            minIndex = v;
        }
    }
    
    return minIndex;
}
/*Implements Dijkstra's shortest path algorithm*/
void dijkstra(Graph* graph, int startVertex) {
    // Validate input parameters
    if (!graph) {
        printf("Error: Graph is NULL\n");
        return;
    }
    if (startVertex < 0 || startVertex >= graph->numVertices) {
        printf("Error: Invalid start vertex. Must be between 0 and %d\n", graph->numVertices - 1);
        return;
    }
    int numVertices = graph->numVertices;
    // Arrays to store shortest distances and visited status
    int* dist = (int*)malloc(numVertices * sizeof(int));
    bool* visited = (bool*)malloc(numVertices * sizeof(bool));
    if (!dist || !visited) {
        printf("Error: Memory allocation failed for Dijkstra's algorithm\n");
        free(dist);
        free(visited);
        return;
    }
    // Initialize distances as infinite and visited as false
    for (int i = 0; i < numVertices; i++) {
        dist[i] = INT_MAX;
        visited[i] = false;
    }
    // Distance from source to itself is 0
    dist[startVertex] = 0;
    printf("\n=== Dijkstra's Shortest Path from vertex %d ===\n", startVertex);
    // Find shortest path for all vertices
    for (int count = 0; count < numVertices - 1; count++) {
        // Pick the minimum distance vertex not yet processed
        int u = minDistance(dist, visited, numVertices);
        
        if (u == -1) break;  // All remaining vertices are inaccessible
        
        // Mark the picked vertex as processed
        visited[u] = true;
        Node* temp = graph->adjLists[u];
        while (temp) {
            int v = temp->vertex;
            int weight = temp->weight;
            
            // Update dist[v] if not visited, there's an edge from u to v,
            // and total weight of path from start to v through u is smaller
            if (!visited[v] && dist[u] != INT_MAX && 
                dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
            }
            temp = temp->next;
        }
    }
    // Print the shortest distances
    printf("Vertex\tDistance from Source\n");
    for (int i = 0; i < numVertices; i++) {
        if (dist[i] == INT_MAX) {
            printf("%d\t\tINFINITE\n", i);
        } else {
            printf("%d\t\t%d\n", i, dist[i]);
        }
    }
    printf("==========================================\n\n");
    // Free allocated memory
    free(dist);
    free(visited);
}