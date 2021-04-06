// Variable Declarations
let origin_location_code = $("#origin_location_code_input");
let origin_location_code_input_group = $("#origin_location_code_input-group");
let destination_location_code = $("#destination_location_code_input");
let destination_location_code_input_group = $("#destination_location_code_input-group");
let all_route = $("#id_all_route");
let all_route_label = $("#all_route-label");
let coupon_code = $("#coupon_code_input");
let cut_off_value = $("#id_cut_off_value");
let max_value = $("#id_max_value");
let generate_coupon_btn = $("#generate_coupon");


// Dynamic Route

all_route.change(function () {
    if (this.checked == true) {
        origin_location_code.val("");
        origin_location_code_input_group.addClass("hidden");
        destination_location_code.val("");
        destination_location_code_input_group.addClass("hidden");
        // console.log("Check box is checked");
    } else {
        origin_location_code_input_group.removeClass("hidden");
        destination_location_code_input_group.removeClass("hidden");
        // console.log("Check box is Unchecked");
    }
});

// Auto Generate Coupon Code

function generate_random_code(length) {
   var result           = '';
   var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
   var charactersLength = characters.length;
   for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}

generate_coupon_btn.click(function () {
    let generated_code = generate_random_code(7);
    coupon_code.val(generated_code);
    // console.log("Auto Generate Button Clicked");
});