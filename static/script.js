const BASE_URL = "http://localhost:5000/api";


/** given data about a cupcake, generate html */

function generateCupcakeHTML(cupcake) {
  return `
<div class="container pet-container">
    <div class="row">
      <div class="col-3">
        <img class="pet-img" src="${ cupcake.image }" alt="image of Cupcake" />
      </div>
      <div class="col-9">
        <p class="pet-title">Flavor: ${ cupcake.flavor }</p>
        <p class="pet-details">Size: ${ cupcake.size }</p>
        <p class="pet-details">Rating: ${ cupcake.rating }</p>
        <button class="btn btn-sm btn-danger delete-button" data-id="${cupcake.id}">X</button>
      </div>
    </div>
  </div>
  `;
}


/** put initial cupcakes on page. */

async function showInitialCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeData));
    $("#cupcakes-list").append(newCupcake);
  }
}


/** handle form for adding of new cupcakes */

$("#new-cupcake-form").on("submit", async function (evt) {
  evt.preventDefault();

  let flavor = $("#form-flavor").val();
  let rating = $("#form-rating").val();
  let size = $("#form-size").val();
  let image = $("#form-image").val();

  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  });

  let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
  $("#cupcakes-list").append(newCupcake);
  $("#new-cupcake-form").trigger("reset");
});


/** handle clicking delete: delete cupcake */

$("#cupcakes-list").on("click", ".delete-button", async function (e) {
  e.preventDefault();

  const cupcake = e.target.parentElement.parentElement.parentElement
  const id = e.target.dataset.id

  await axios.delete(`${BASE_URL}/cupcakes/${id}`);
  cupcake.remove();
});


showInitialCupcakes();
