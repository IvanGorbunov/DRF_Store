$(document).ready( function () {
    $('#table_id').DataTable();
} );

let tds = document.querySelectorAll('td');
for (let i = 0; i < tds.length; i++){

    // get products
    tds[i].addEventListener('click', function (){
        let url = this.attributes['data-url'];
        console.log(url);
        ajax({
            url: url,
            method: "GET",
            data: {
              button_text: $(this).text()
            },
            success: function (response) {
                $("#data").html(response);
            }
        });
    });

    // input values
    tds[i].addEventListener('dblclick', function fInput(){
       let input = document.createElement('input');
       input.value = this.innerHTML;
       this.innerHTML = '';
       this.appendChild(input);

       let td = this
       input.addEventListener('blur', function (){
           td.innerHTML = this.value;
           td.addEventListener('dblclick', fInput);
        });

       this.removeEventListener('dblclick', fInput);
    });


}