export const getDefaultProductSellerModel = () => ({
    id: null,
    idProduct: null,
    idSeller: null,
    name: "",
    description: "",
    specSheet: "",
    ecoPoints: 0,
    images: [],
    price: 0,
    shippingCosts: 0,
    quantity: 0,
    stock: 0,
    category: "",
    type: "",
    brand: "",
    age_restricted: false
});

export const createProductSellerFromApiResponse = (apiResponse) => ({
    id: apiResponse.id || getDefaultProductSellerModel().id,
    idProduct: apiResponse.id_product || getDefaultProductSellerModel().idProduct,
    idSeller: apiResponse.id_seller || getDefaultProductSellerModel().idSeller,
    name: apiResponse.name || getDefaultProductSellerModel().name,
    description: apiResponse.description || getDefaultProductSellerModel().description,
    specSheet: apiResponse.spec_sheet || getDefaultProductSellerModel().specSheet,
    ecoPoints: apiResponse.eco_points || getDefaultProductSellerModel().ecoPoints,
    images: apiResponse.images || getDefaultProductSellerModel().images,
    price: apiResponse.price || getDefaultProductSellerModel().price,
    shippingCosts: apiResponse.shipping_costs || getDefaultProductSellerModel().shippingCosts,
    quantity: apiResponse.quantity || getDefaultProductSellerModel().quantity,
    stock: apiResponse.stock || getDefaultProductSellerModel().stock,
    category: apiResponse.category || getDefaultProductSellerModel().category,
    type: apiResponse.type || getDefaultProductSellerModel().type,
    brand: apiResponse.brand || getDefaultProductSellerModel().brand,
    age_restricted: apiResponse.age_restricted || getDefaultProductSellerModel().age_restricted
});
