var updateBtns=document.getElementsByClassName('update-cart')

for(var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        var productId=this.dataset.product
        var action =this.dataset.action
        console.log('productId:',productId, 'action:',action)

        console.log('USER:', user)      //Prikaz logovanog i gost korisnika u konzoli
        if(user === 'AnonymousUser'){
            console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data...')

    var url='/update_item/'

    fetch(url, {                     //Slanje podataka na url i određeni tip podataka koji šaljemo
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) =>{
        return response.json()
    })

    .then((data)=>{
        console.log('data:',data)       //Ispisivanje podataka iz json requesta koji smo definirali prije nakon sto smo to pretvorili u json
        location.reload()
    })
}