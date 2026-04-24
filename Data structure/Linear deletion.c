#include <stdio.h>
#include <stdbool.h>

#define MaxSize 50      // 定义顺序表的最大容量
typedef int ElemType;   // 假设元素类型是 int，方便修改

// 定义顺序表结构体
typedef struct {
    ElemType data[MaxSize]; // 静态数组存放数据
    int length;             // 当前长度
} SqList;

/**
 * 删除顺序表 L 中第 i 个位置的元素 (i 为位序，从 1 开始)
 * @param L 顺序表引用
 * @param i 要删除的位序
 * @param e 用于返回被删除的元素值
 * @return true 删除成功, false 删除失败
 */
bool ListDelete(SqList *L, int i, ElemType *e) {
    // 1. 判断 i 的范围是否有效 (这是最严谨的写法)
    // 注意：如果传入的是指针 L->length，如果是引用则是 L.length
    if (i < 1 || i > L->length) {
        return false;
    }

    // 2. 保存被删除元素的值
    // 将位序 i 转换为下标 i-1
    *e = L->data[i - 1];

    // 3. 将第 i 个位置之后的所有元素前移
    // 这里的逻辑是：从被删除元素的下一个元素开始（下标 i），直到最后一个元素（下标 L->length - 1）
    for (int j = i; j < L->length; j++) {
        L->data[j - 1] = L->data[j];
    }

    // 4. 表长减 1
    L->length--;

    return true;
}