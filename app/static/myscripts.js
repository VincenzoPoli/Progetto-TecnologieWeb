function changeState(btn1_id, btn2_id, input1_id, input2_id) {
    let btn1_radio, btn2_radio, input1, input2
    btn1_radio = document.getElementById(btn1_id)
    btn2_radio = document.getElementById(btn2_id)
    input1 = document.getElementById(input1_id)
    input2 = document.getElementById(input2_id)
    if (btn1_radio.checked) {
        input1.removeAttribute("disabled")
        input2.setAttribute("disabled", "")
    }

    if (btn2_radio.checked) {
        input2.removeAttribute("disabled")
        input1.setAttribute("disabled", "")
    }
}
function editPost(btn_el, id) {

    btn_el.setAttribute("hidden", true)

    let div_el, right_button, body_el, form_el, text_el, submit_el, content

    div_el = document.getElementById(id)
    body_el = document.getElementById(id).children[0]
    content = body_el.innerHTML
    div_el.removeChild(body_el)

    form_el = document.createElement("form")
    form_el.setAttribute("action", "/edit_post/" + id)
    form_el.setAttribute("method", "post")

    text_el = document.createElement("textarea")
    text_el.setAttribute("rows", "4")
    text_el.setAttribute("name", "new_body")
    text_el.value = content

    right_button = document.createElement("div")
    right_button.setAttribute("class", "button-right")

    submit_el = document.createElement("button")
    submit_el.setAttribute("type", "submit")
    submit_el.setAttribute("class", "btn btn-outline-primary")
    submit_el.innerHTML = "Applica"

    div_el.appendChild(form_el)
    form_el.appendChild(text_el)
    form_el.appendChild(right_button)
    right_button.appendChild(submit_el)
}
function alertDeletingProfile() {
    if (confirm("Sei sicuro di voler cancellare il tuo account? Non potrai più tornare indietro.")) {
        window.location.href = "{{ url_for('delete_user') }}"
    } else {
      // Non fare niente!
    }
}
function textFormatting(id) {
    let textBody, content, highlighted
    textBody = document.getElementById("body-textarticle")
    highlighted = window.getSelection().toString()
    content = textBody.value
    if (id === "bold") {
        if (highlighted) {
            textBody.value = content.replace(highlighted, "<b>" + highlighted + "</b>")
        } else {
            textBody.value = content + "<b></b>"
        }
    } else if (id === "italic") {
        if (highlighted) {
            textBody.value = content.replace(highlighted, "<i>" + highlighted + "</i>")
        } else {
            textBody.value = content + "<i></i>"
        }
    } else if (id === "underline") {
        if (highlighted) {
            textBody.value = content.replace(highlighted, "<u>" + highlighted + "</u>")
        } else {
            textBody.value = content + "<u></u>"
        }
    }
}

function showPreview() {
    let x
    x = document.getElementById("preview-container")
    x.removeAttribute("style", "display: block")
}