import axiosInstance from '../AxiosInstance';

const addEstimatedDate = async (product_line_id, date) => {
    try {
        console.log("date:", date);
        const response = await axiosInstance.post(`/product_lines/me/${product_line_id}`, date);
        console.log("GUARDADO DE FECHA:", response);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al agregar la fecha estimada', error.response ? error.response.data : error);
        throw error;
    }
};

const getProductLines = async () => {
    try {
        const response = await axiosInstance.get('/product_lines/me/');
        console.log("PRODUCT LINES:", response);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener los product lines', error.response ? error.response.data : error);
        throw error;
    }
};

export { addEstimatedDate, getProductLines };
