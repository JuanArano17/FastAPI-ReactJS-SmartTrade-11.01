import axiosInstance from '../AxiosInstance';

const evaluateSellerProductById = async (product) => {
    console.log("evaluate: ", product)
    let formatedProduct;
    if (product.state == "Approved"){
        formatedProduct = {
            eco_points: product.eco_points,
            age_restricted: product.age_restricted,
            state: product.state
        };
    }else {
        formatedProduct = {
            justification: product.justification,
            state: product.state
        };
    }
    try {
        console.log(`Intentando editar el producto con id: ${product.id}...`);
        const response = await axiosInstance.put(`/seller_products/${product.id}`, formatedProduct);
        console.log("producto editado correctamente", response);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al editar el producto', error.response ? error.response.data : error);
    }
}
const getPendingProducts = async () => {
    try {
        console.log("Intentando conseguir todos los productos a evaluar...");
        const response = await axiosInstance.get('/admin/seller-products');
        console.log("respuesta api", response);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener los productos', error.response ? error.response.data : error);
        throw error;
    }
};
export {evaluateSellerProductById, getPendingProducts}