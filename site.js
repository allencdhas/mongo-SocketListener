const socket = new WebSocket("ws://localhost:8000");

socket.onopen = function (e) {
  console.log("WebSocket connection established");
};

socket.onmessage = function (event) {
  console.log(`Data received: ${event.data}`);
};

socket.onclose = function (event) {
  if (event.wasClean) {
    console.log("WebSocket connection closed cleanly");
  } else {
    console.log("WebSocket connection died");
  }
};

socket.onerror = function (error) {
  console.log(`WebSocket error: ${error}`);
};
