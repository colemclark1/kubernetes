<template>
  <div class="home">
    <p>Home</p>
    {{ msg }}
    <h1>Users</h1>
    <div v-for="user in users" :key="user.id" class="user">
      <h2>{{ user.firstName }} {{ user.lastName }}</h2>
    </div>
    <div>
    <label for="firstName">First Name</label>
    <input id='firstName' placeholder="first name"/>
    </div>

    <div>
    <label for="lastName">Last Name</label>
    <input id='lastName' placeholder="last name"/>
    </div><div>
        <label for="email">Email</label>
    <input id="email" placeholder="email"/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  props: {
    msg: String
  },
  data() {
    return {
      users: []
    }
  },
  mounted() {
    fetch('http://localhost:5000/user', {method: "GET", headers: {
               "Content-Type": "application/json"
           }})
      .then(res => res.json())
      .then(data => this.users = data)
      .catch(err => console.log(err.message))
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
