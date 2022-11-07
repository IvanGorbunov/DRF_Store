$(document).ready( function () {

    $('#table_id').DataTable();

    $('#table_id').on('click', '.row-grouping', function () {

        let dataId = $(this).data('id');

        $.ajax({
            url: 'api/store/orders/' + dataId + '/',
            type: 'get',
            success: function (response) {

                console.log(response);

                let row = $('#row[data-id="' + dataId + '"]');
                let index = row.index();
                console.log('ind = ' + index);
                let table = document.getElementById('tbody_id');

                console.log(response.items.length)

                for (let i = 1; i <= response.items.length; i++) {

                    let newRow = table.insertRow(index + i);

                    let newCell_0 = newRow.insertCell(0);
                    let newCell_1 = newRow.insertCell(1);
                    let newCell_2 = newRow.insertCell(2);
                    let newCell_3 = newRow.insertCell(3);

                    newCell_0.className = 'td';
                    newCell_1.className = 'td';
                    newCell_2.className = 'td';
                    newCell_3.className = 'td';

                    let newText = document.createTextNode(i);
                    newCell_0.appendChild(newText);

                    newText = document.createTextNode(response.items[i-1].product.title);
                    newCell_1.appendChild(newText);

                    newCell_2.setAttribute('colSpan', '2');
                    let text = 'quantity: ' + response.items[i-1].quantity + ' price: ' + response.items[i-1].price;
                    newText = document.createTextNode(text);
                    newCell_2.appendChild(newText);

                    newText = document.createTextNode(response.items[i-1].amount);
                    newCell_3.appendChild(newText);

                };
            }
        });
    });
} );

