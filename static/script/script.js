const bv = document.querySelectorAll(".bv")
const mv = document.querySelectorAll(".mv")
const row = document.querySelectorAll(".stock-row")

for (let i = 0; i < bv.length; i++){
    if (bv[i].innerHTML <= mv[i].innerHTML){
        row[i].classList.add("plus")
    }
    else{
        row[i].classList.add("minus")
    }
}

function validateForm() {
    let pw = document.forms["signup"]["password"].value;
    let pw_clone = document.forms["signup"]["password_clone"].value;
    if (pw !== pw_clone) {
      alert("Password not match");
      return false;
    }
  }
