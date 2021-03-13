<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: "Noto Sans KR", sans-serif;
}
html {
  scroll-behavior: smooth;
}
:host {
  display: inline-block;
  z-index: 1000;
  max-height: calc(100vh - 5vh);
  display: flex;
  flex-direction: column;
  color: #3c4043;
}

#menu-holder {
  position: relative;
  padding: 20px;
  width: 200px;
  display: flex;
  cursor: pointer;
  border-radius: 0 10px 10px 10px;
  background: var(--menu-holder-closed-background, #fff);
  box-shadow: var(
    --menu-holder-closed-box-shadow,
    0 2px 5px rgba(0, 0, 0, 0.3)
  );
}

#menu-holder:focus {
  outline: 0;
}

#menu-holder:focus:after {
  content: "";
  position: absolute;
  top: -2px;
  left: -2px;
  height: 100%;
  width: 100%;
  border-radius: inherit;
  border: 2px solid #8ab4f8;
  z-index: 1;
}

#app-name {
  font-family: "BoingSemiBold", Helvetica, Arial, sans-serif;
  font-size: 24px;
  line-height: 28px;
  font-weight: 500;
  color: #1967d2;
  opacity: var(--app-name-closed-opacity, 1);
}

#hamburger-menu-icon {
  display: inline-block;
  vertical-align: middle;
}

#main-menu {
  border-top: 1px solid #bdc1c6;
  /* width: 305px; */
  display: none;
  width: 100%;
  overflow-y: auto;
  border-radius: 0 0px 10px 10px;
  background: var(--main-menu-background, #fff);
  box-shadow: var(--main-menu-box-shadow, 0 4px 5px rgba(0, 0, 0, 0.3));
  max-height: calc(100vh - 100px);
}

:host([open]) #main-menu {
  display: block;
}

svg {
  padding-right: 10px;
}

svg > path {
  fill: #3c4043;
}

/* ul {
  list-style: none;
  padding-left: 0;
  border-bottom: 1px solid #dadce0;
  padding-bottom: 10px;
}

ul:last-child {
  border-bottom: 0;
  padding-bottom: 0;
}

li {
  cursor: pointer;
  padding: 10px 0;
  background: transparent;
  border: 0;
  outline: 0;
  padding-left: 18px;
  display: flex;
  align-items: center;
}
li:focus {
  outline: 2px solid var(--focus-color);
}

li:last-child {
  margin-bottom: 0;
}

li svg {
  padding-right: 12px;
}

li:hover {
  background-color: #e8f0fe;
  color: #1967d2;
}

li:hover svg > path {
  fill: #1967d2;
} */

#model-name {
  font-size: 16px;
  padding: 8px 18px 0px 18px;
  display: flex;
  align-items: center;
}

#model-name svg {
  width: 18px;
  height: 18px;
  padding-left: 10px;
  padding-right: 0;
}

#model-name svg path {
  fill: #9aa0a6;
}

#model-name > * {
  /* display: flex; */
  cursor: pointer;
  word-wrap: break-word;
}

#model-name > *:hover,
#model-name > *:hover path {
  color: #1967d2;
  fill: #1967d2;
}

[disabled] {
  color: var(--disabled-color, #c9c9c9);
  cursor: default;
}
[disabled]:hover {
  color: var(--disabled-color, #c9c9c9);
  background: none;
}
[disabled]:hover svg > path {
  fill: var(--disabled-color, #c9c9c9);
}
[disabled] svg > path {
  fill: var(--disabled-color, #c9c9c9);
}

:host([disableDriveView]) #model-name {
  display: none;
}
</style>
