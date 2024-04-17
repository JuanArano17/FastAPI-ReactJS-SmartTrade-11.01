export const getDefaultProductModel = () => ({
    id: null,
    name: "",
    description: "",
    specSheet: "",
    ecoPoints: 0,
    stock: 0,
});

export const createProductFromApiResponse = (apiResponse) => ({
    id: apiResponse.id || getDefaultProductModel().id,
    name: apiResponse.name || getDefaultProductModel().name,
    description: apiResponse.description || getDefaultProductModel().description,
    specSheet: apiResponse.spec_sheet || getDefaultProductModel().specSheet,
    ecoPoints: apiResponse.eco_points || getDefaultProductModel().ecoPoints,
    stock: apiResponse.stock || getDefaultProductModel().stock,
});
