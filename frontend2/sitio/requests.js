var requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };

  fetch('http://localhost:5000/getMyInfo', requestOptions)
  .then(res => {
    if (!res.ok) {
      alert("HTTP error! status:" + res.status);
    }
    return res.json();
  })
  .then(json => {
    document.getElementById("response").textContent = "Hola " + json.response;
    
  })
  .catch(error => alert("error: " + error));