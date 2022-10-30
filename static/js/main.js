let tds = document.querySelectorAll('td');
for (let i = 0; i < tds.length; i++){
    tds[i].addEventListener('click', function fInput(){
       let input = document.createElement('input');
       input.value = this.innerHTML;
       this.innerHTML = '';
       this.appendChild(input);

       let td = this
       input.addEventListener('blur', function (){
           td.innerHTML = this.value;
           td.addEventListener('click', fInput);
        });

       this.removeEventListener('click', fInput);
    });
}