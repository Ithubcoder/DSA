#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STUDENTS 100

typedef struct {
    int id;
    char name[100];
    float gpa;
} Student;

Student students[MAX_STUDENTS];
int student_count = 0;

void addStudent(int id, char* name, float gpa);
void displayStudents();
int findStudentById(int id);
void saveToFile();
void loadFromFile();
void menu();

void addStudent(int id, char* name, float gpa) {
    if (student_count < MAX_STUDENTS) {
        students[student_count].id = id;
        strcpy(students[student_count].name, name);
        students[student_count].gpa = gpa;
        student_count++;
    } else {
        printf("Student list is full.\n");
    }
}

void displayStudents() {
    for (int i = 0; i < student_count; i++) {
        printf("ID: %d\nName: %s\nGPA: %.2f\n\n", students[i].id, students[i].name, students[i].gpa);
    }
}

int findStudentById(int id) {
    for (int i = 0; i < student_count; i++) {
        if (students[i].id == id) {
            return i;
        }
    }
    return -1;
}

void saveToFile() {
    FILE* file = fopen("students.txt", "w");
    if (file == NULL) return;
    for (int i = 0; i < student_count; i++) {
        fprintf(file, "%d,%s,%.2f\n", students[i].id, students[i].name, students[i].gpa);
    }
    fclose(file);
}

void loadFromFile() {
    FILE* file = fopen("students.txt", "r");
    if (file == NULL) return;
    int id;
    char name[100];
    float gpa;
    while (fscanf(file, "%d,%99[^,],%f\n", &id, name, &gpa) != EOF) {
        addStudent(id, name, gpa);
    }
    fclose(file);
}

void menu() {
    int choice, id;
    char name[100];
    float gpa;
    loadFromFile();
    while (1) {
        printf("Student Records Management System\n");
        printf("1. Add Student\n");
        printf("2. View Students\n");
        printf("3. Find Student by ID\n");
        printf("4. Save and Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                printf("Enter student ID: ");
                scanf("%d", &id);
                printf("Enter student name: ");
                scanf(" %[^\n]", name);
                printf("Enter student GPA: ");
                scanf("%f", &gpa);
                addStudent(id, name, gpa);
                break;
            case 2:
                displayStudents();
                break;
            case 3:
                printf("Enter student ID to find: ");
                scanf("%d", &id);
                int index = findStudentById(id);
                if (index != -1) {
                    printf("ID: %d\nName: %s\nGPA: %.2f\n\n", students[index].id, students[index].name, students[index].gpa);
                } else {
                    printf("Student not found.\n");
                }
                break;
            case 4:
                saveToFile();
                exit(0);
            default:
                printf("Invalid choice!\n");
        }
    }
}

int main() {
    menu();
    return 0;
}
