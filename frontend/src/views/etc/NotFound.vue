<template>
  <div class="container">
    <div class="boo-wrapper">
      <div class="boo">
        <div class="face"></div>
      </div>
      <div class="shadow"></div>

      <h1>Whoops!</h1>
      <p>
        해당 태그의 게시글이
        <br />존재하지않습니다.
      </p>
    </div>
  </div>
</template>
<script>
export default {
  created() {
    setTimeout(() => this.$router.push({path: "/"}), 5000);
  },
};
</script>
<style scoped>
h1 {
  text-align: center;
}
p {
  text-align: center;
}
</style>
