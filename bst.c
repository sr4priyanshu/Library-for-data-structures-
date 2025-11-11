#include "dshelp.h"
tree* bst_insert(tree* root, int x)
{
    if (root == NULL) 
    {
        tree* ptr = (tree*)(malloc(sizeof(tree)));
        ptr->right = NULL;
        ptr->data = x;
        ptr->left = NULL;
        root = ptr;
    } 
    else 
    {
        if (x < root->data) 
        {
            root->left = bst_insert(root->left, x);  
        } 
        else if (x > root->data) 
        {
            root->right = bst_insert(root->right, x);  
        }
    }
    return root;
}
void bst_displayPostorder(tree* root) 
{
    if (root != NULL) 
    {
        bst_displayPostorder(root->left);  
        bst_displayPostorder(root->right);  
        printf("%d ", root->data);
    }
}
void bst_displayPreorder(tree* root) 
{
    if (root != NULL) 
    {
        printf("%d ", root->data);
        bst_displayPreorder(root->left);  
        bst_displayPreorder(root->right);  
    }
}
void bst_displayInorder(tree* root) 
{
    if (root != NULL) 
    {
        bst_displayInorder(root->left);  
        printf("%d ", root->data);
        bst_displayInorder(root->right);  
    }
}
int bst_countNodes(tree* root, int c) 
{
    if (root != NULL) 
    {
        c = bst_countNodes(root->left, c);  
        c = c + 1;
        c = bst_countNodes(root->right, c);  
    }
    return c;
}
int bst_One_child(tree* root, int c) 
{
    if (root != NULL) 
    {
        c = bst_One_child(root->left, c); 
        if ((root->left == NULL && root->right != NULL) || (root->right == NULL && root->left != NULL))
            c = c + 1;
        c = bst_One_child(root->right, c); 
    }
    return c;
}
int bst_Two_child(tree* root, int c) 
{
    if (root != NULL) 
    {
        c = bst_Two_child(root->left, c);
        if (root->right != NULL && root->left != NULL)
            c = c + 1;
        c = bst_Two_child(root->right, c);
    }
    return c;
}
int bst_Common_Parent(tree* root, int c) 
{
    if (root != NULL) 
    {
        c = bst_Common_Parent(root->left, c);
        if (root->right != NULL && root->left != NULL)
            c = c + 1;
        c = bst_Common_Parent(root->right, c);
    }
    return c;
}
tree* bst_Delete_Node(tree* root, int key)
{
    if (root == NULL)
    {
        printf("NODE NOT FOUND\n");
        return NULL;
    }

    if (key < root->data)
        root->left = bst_Delete_Node(root->left, key);
    else if (key > root->data)
        root->right = bst_Delete_Node(root->right, key);
    else
    {
        // Node found
        if (root->left == NULL)
        {
            tree* temp = root->right;
            free(root);
            return temp;
        }
        else if (root->right == NULL)
        {
            tree* temp = root->left;
            free(root);
            return temp;
        }
        tree* temp = root->right;
        while (temp->left != NULL)
            temp = temp->left;

        root->data = temp->data; 
        root->right = bst_Delete_Node(root->right, temp->data);
    }
    return root;
}
