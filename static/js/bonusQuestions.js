// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    // console.log(items)
    console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table

    let filter1 = "!"
    let filter2 = "Description:"
    let filter3 = "!Description:"

    let result = []

    if (filterValue.startsWith(filter3)){
        for (let element of items) {
            if (!element['Description'].toLowerCase().includes(filterValue.replace(filter3,"").toLowerCase())){
                result.push(element)
                console.log(result)}}
        return result
    } else if (filterValue.startsWith(filter2)){
        for (let element of items) {
            if (element['Description'].toLowerCase().includes(filterValue.replace(filter2,"").toLowerCase())) {
                result.push(element)
                console.log(result)}}
        return result
    } else if (filterValue.startsWith(filter1)){
        for (let element of items) {
            if (!element['Title'].toLowerCase().includes(filterValue.replace(filter1,"").toLowerCase())) {
                result.push(element)
                console.log(result)}}
        return result
    } else {
        for (let element of items) {
            if (element['Title'].toLowerCase().includes(filterValue.toLowerCase())) {
                result.push(element)
                console.log(result)}}
        return result
    }
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    console.log("increaseFont")
}

function decreaseFont() {
    console.log("decreaseFont")
}
