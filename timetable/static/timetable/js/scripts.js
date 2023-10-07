// Принимает фразу из формы поиска и таблицу, в которой поиск осуществляется.
// Скрывает те строки таблицы, в которой не найдена фраза.
function SearchObject(phrase, table) {
    let regPhrase = new RegExp(phrase.value, "i");
    let flag = false;
    for (let i = 1; i < table.rows.length; i++) {
        flag = false;
        for (let j = table.rows[i].cells.length - 1; j >= 0; j--) {
            flag = regPhrase.test(table.rows[i].cells[j].innerHTML);
            if (flag) break;
        }
        if (flag) {
            table.rows[i].style.display = "";
        } else {
            table.rows[i].style.display = "none";
        }
    }    
}

// Поиск в таблице со всеми группами
function tableSearchGroup() {
    let phrase = document.getElementById("search-group");
    let table = document.getElementById("group-table");
    SearchObject(phrase, table);
}

// Поиск в таблице со всеми преподавателями
function tableSearchTutor() {
    let phrase = document.getElementById("search-tutor");
    let table = document.getElementById("tutor-table");
    SearchObject(phrase, table);
}

// Поиск в таблице со всеми дисциплинами
function tableSearchSubject() {
    let phrase = document.getElementById("search-subject");
    let table = document.getElementById("subject-table");
    SearchObject(phrase, table);
}

// Поиск в таблице со всеми типами занятий
function tableSearchWorkType() {
    let phrase = document.getElementById("search-work-type");
    let table = document.getElementById("work-type-table");
    SearchObject(phrase, table);
}

// Поиск в таблице со всеми аудиториями
function tableSearchClassroom() {
    let phrase = document.getElementById("search-classroom");
    let table = document.getElementById("classroom-table");
    SearchObject(phrase, table);
}