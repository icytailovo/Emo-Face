import React, {useState} from 'react';
import {Button, Container, TextField, Typography, Grid, Alert, CircularProgress} from '@mui/material';
import Box from "@mui/material/Box";
import AddAPhotoIcon from '@mui/icons-material/AddAPhoto';
import "../src/App.css";

const Upload = () => {
    const [file, setFile] = useState(null);
    const [imageURL, setImageURL] = useState(null);
    const [newImages, setNewImages] = useState([]);
    const [text, setText] = useState("");
    const [alert, setAlert] = useState(false);
    const [progress, setProgress] = useState(false);

    const handleChange = (e) => {
        console.log(e.target.files[0]);
        let file = e.target.files[0];
        setFile(e.target.files[0]);
        let url = URL.createObjectURL(file);
        console.log(url);
        setImageURL(url);
    };

    const handleClick = async (e) => {
        if (file !== null && text !== "") {
            setAlert(false);
            setNewImages([]);
            setProgress(true);

            let query = "http://localhost:8080?path=" + file.name + "&prompt=" + text;
            console.log(query);
            try {
                let response = await fetch(query);
                if (!response.ok) {
                    // get error message from body or default to response statusText
                    const error = (data && data.message) || response.statusText;
                    return Promise.reject(error);
                }
                const data = await response.json();
                console.log(data);
                let tempList = [];
                console.log(data.image);
                let index = 0;
                for (let newImage of data) {
                    let blob = new Blob([new Uint8Array(newImage.image)],{type:'image/png'});
                    let newFile = new File([blob], "haha" + index);
                    let url = URL.createObjectURL(newFile);
                    tempList.push({url: url});
                    index++;
                }
                console.log(tempList);
                setNewImages(tempList);
                setProgress(false);
            } catch (error) {
                console.error('There was an error!', error);
            }
        } else {
            setAlert(true);
        }
    }

    return (
        <Container fixed>
            <Box>
                <Typography variant="h4" sx={{py: 2}}>
                    Emo Face
                </Typography>
                <Box sx={{
                    height: 600,
                    width: 900,
                    border: 1,
                    borderRadius: 8,
                    textAlign: "center",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center"
                }}>
                    {
                        imageURL &&
                        <img src={imageURL} alt="images gallery" loading="lazy" className={"upload_img"}/>
                    }
                </Box>
                <Button variant="contained" component="label" startIcon={<AddAPhotoIcon />}
                        sx={{my: 2}}>
                    Upload An Image
                    <input hidden accept="image/*" type="file" onChange={handleChange} />
                </Button>

                <Typography variant="body" component="div" sx={{pb: 2}}>
                    Simply describe the image with what kind of emoji to replace with your face.
                </Typography>
                <Grid container spacing={2} justifyContent="center"
                      alignItems="center">
                    <Grid item xs={8}>
                        <TextField fullWidth id="outlined-basic" label="Description of the image" variant="outlined"
                                   onChange={(e) => setText(e.target.value)}/>
                    </Grid>
                    <Grid item xs={4}>
                        <Button variant="contained" onClick={handleClick}>Generate!</Button>
                    </Grid>
                </Grid>

                {
                    (!alert) ?
                    <></>
                    :
                    <Box py={1} sx={{width: 450}}>
                        <Alert severity={"warning"}>Please provide an image and a text description.</Alert>
                    </Box>
                }

                {
                    (!progress) ?
                        <></>
                        :
                        <Box py={1} sx={{ display: 'flex' }}>
                            <CircularProgress />
                        </Box>
                }

                {
                    newImages.length !== 0 &&
                    <Box>
                        <Typography variant="h5" component="div" sx={{py: 2}}>
                            Generated Images Result
                        </Typography>
                        <Grid container spacing={2} sx={{width: 1000}}>
                            {
                                newImages.map((file, index) => (
                                <Grid item xs={4} key={index}>
                                    <img src={file.url} alt="images gallery" loading="lazy" className={"new_img"} />
                                </Grid>
                                ))
                            }
                        </Grid>
                    </Box>
                }
            </Box>
            <Box py={5}>

            </Box>
        </Container>
    );
};

export default Upload;