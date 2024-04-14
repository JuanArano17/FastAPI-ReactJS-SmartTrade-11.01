const styles = {
    mainBox: {
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh'
    },
    paperContainer: {
        p: 4,
        boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.2)',
        borderRadius: '20px',
        mb: '80px',
        mt: '40px',
        borderColor: 'black',
        borderWidth: '3px',
        borderStyle: 'solid'
    },
    registerButton: {
        mt: 3,
        mb: 2,
        bgcolor: '#dfedd6',
        color: '#232323',
        boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.2)',
        borderRadius: '10px',
    },
    formContainer: { mt: 3 },
    rounded_img: {
        width: '200px',
        height: 'auto',
        marginBottom: '20px',
        margin: '0 auto',
        borderRadius: '50%',
        boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.2)'
    },
    imageStyle: {
        width: '275px',
        height: 'auto',
        border: '2px solid black',
        borderRadius: '15px',
    },
    greenRoundedButton: {
        bgcolor: '#cbe8ba',
        color: '#000000',
        fontWeight: 'bold',
        marginBottom: '20px',
        boxShadow: '-5px 5px 3px rgba(0, 0, 0, 0.4)',
        width: '100%',
        borderRadius: '15px'
    },
    textfields: {
        borderColor: 'black',
        borderWidth: '1px',
        borderStyle: 'solid',
        borderRadius: '5px',
        backgroundColor: 'white',
    },
    mainContainer: {
        mt: 4,
        mb: 4,
        flex: 1
    },
    headerText: {
        color: "#629c44",
        fontWeight: "bold",
    },
    headerText: {
        fontWeight: "bold",
        color: "#232323",
        display: 'flex',
        alignItems: 'center',
    },
    ThickDivider: {
        backgroundColor: "#232323",
        height: "2px",
        margin: "20px 0",
    },
    clearFiltersButtonStyle: {
        minWidth: '120px',
        border: '1px solid #000',
        borderRadius: '4px',
        backgroundColor: '#fff',
        color: '#000',
        padding: '6px 16px',
        '&:hover': {
            backgroundColor: '#f5f5f5',
        },
    },
    paperContainerdos: {
        display: 'flex',
        alignItems: 'center',
        padding: 2,
        marginBottom: 2,
        p: 4,
        boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.2)',
        borderRadius: '20px',
        mb: '80px',
        mt: '40px',
        borderColor: 'black',
        borderWidth: '1px',
        borderStyle: 'solid'
    },
    totalPriceBox: {
        borderColor: 'black',
        borderWidth: '1px',
        borderRadius: '20px',
        borderStyle: 'solid',
        backgroundColor: '#cbe8ba',
        padding: '10px 20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        mb:2,
    },
    cartItemPaper: {
        display: 'flex',
        justifyContent: 'space-between',
        marginBottom: 2,
        padding: '16px',
        alignItems: 'center',
        borderColor: 'black',
        borderWidth: '2px',
        borderRadius: '20px',
        borderStyle: 'solid',
    },
    productImage: {
        width: 100,
        marginRight: 16
    },
}
export default styles;
