import React, { useState } from 'react';
import { Box, ButtonBase } from '@mui/material';

const ImageSelector = ({ images }) => {
    const [imageIndex, setImageIndex] = useState(0);
    const [isZoomed, setIsZoomed] = useState(false);
    const [zoomPosition, setZoomPosition] = useState({ x: 0, y: 0 });

    const handleImageChange = (newIndex) => {
        setImageIndex(newIndex);
        setIsZoomed(false); // Reset zoom when changing image
    };

    const handleMouseMove = (e) => {
        if (isZoomed) {
            const { left, top, width, height } = e.currentTarget.getBoundingClientRect();
            const x = ((e.pageX - left) / width) * 100;
            const y = ((e.pageY - top) / height) * 100;
            setZoomPosition({ x, y });
        }
    };

    const toggleZoom = () => {
        setIsZoomed(!isZoomed);
    };

    return (
        <Box sx={{ display: 'flex' }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', mr: 2 }}>
                {images.map((img, idx) => (
                    <ButtonBase key={idx} onClick={() => handleImageChange(idx)} sx={{ mb: 1 }}>
                        <img
                            src={img}
                            alt={`Thumbnail ${idx + 1}`}
                            style={{
                                width: '80px',
                                height: '80px',
                                objectFit: 'cover',
                                borderRadius: '8px',
                                border: imageIndex === idx ? '2px solid green' : '2px solid transparent'
                            }}
                        />
                    </ButtonBase>
                ))}
            </Box>
            <Box
                sx={{
                    width: 600,
                    height: 600,
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    overflow: 'hidden',
                    borderRadius: '40px',
                    position: 'relative'
                }}
                onMouseMove={handleMouseMove}
                onClick={toggleZoom}
            >
                <img
                    src={images[imageIndex]}
                    alt={`Image ${imageIndex + 1}`}
                    style={{
                        height: '100%',
                        width: '100%',
                        objectFit: 'cover',
                        objectPosition: 'center center',
                        borderRadius: '40px',
                        boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.7)',
                        transform: isZoomed ? `scale(2)` : 'scale(1)',
                        transformOrigin: `${zoomPosition.x}% ${zoomPosition.y}%`,
                        transition: 'transform 0.3s ease-in-out',
                        cursor: 'zoom-in'
                    }}
                />
            </Box>
        </Box>
    );
};

export default ImageSelector;
