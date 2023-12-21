console.log(location.search)     // lee los argumentos pasados a este formulario
var id=location.search.substr(4)  // paciente_update.html?id=1
console.log(id)
const { createApp } = Vue
  createApp({
    data() {
      return {
        id:0,
        nombre:"",
        apellido:"",
        edad:0,
        imagen:"",
        //url: `http://localhost:5000/paciente/${id}`,
        url:`http://rosario2junio.pythonanywhere.com/paciente/${id}`,
       //url:''+id,
        }  
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    this.id=data.id
                    this.nombre = data.nombre;
                    this.apellido=data.apellido
                    this.edad=data.edad
                    this.imagen=data.imagen                    
                })
                .catch(err => {
                    console.error(err);
                    this.error=true              
                })
        },
        modificar() {
            let paciente = {
                nombre:this.nombre,
                apellido: this.apellido,
                edad: this.edad,
                imagen: this.imagen
            }
            var options = {
                body: JSON.stringify(paciente),
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            }
            fetch(this.url, options)
                .then(function () {
                    alert("Registro modificado")
                    window.location.href = "./paciente.html"; // navega a productos.html          
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Modificar")
                })      
        }
    },
    created() {
        this.fetchData(this.url)
    },
  }).mount('#app')

