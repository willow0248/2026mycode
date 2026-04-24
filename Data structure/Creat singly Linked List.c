#include <stdio.h>
#include <stdlib.h>

typedef struct LNode
{
    int data;
    struct LNode *next;
}LNode,*LinkList;

LinkList creatlinklist(){
    LinkList L=(LinkList)malloc(sizeof(LNode));
    if(L==NULL){
        printf("fail\n");
        exit(1);
    }
    L->next=NULL;
    return L;
}







