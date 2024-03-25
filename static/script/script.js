const bv = document.querySelectorAll(".bv")
const mv = document.querySelectorAll(".mv")
const row = document.querySelectorAll(".stock-row")

for (let i = 0; i < bv.length; i++){
    if (parseInt(bv[i].innerHTML) >= parseInt(mv[i].innerHTML)){
        row[i].classList.add("plus")
    }
    else{
        row[i].classList.add("minus")
    }
}
