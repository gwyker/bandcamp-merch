import React, { useContext, useState } from 'react';
import {
  Grommet,
  Grid,
  Box,
  ResponsiveContext,
  Card,
  CardHeader,
  CardFooter,
  CardBody, Image, Stack,
} from 'grommet';
import './App.css';

const theme = {
  global: {
    colors: {
      brand: '#228BE6',
    },
    font: {
      family: 'Roboto',
      size: '18px',
      height: '20px',
    }
  }
}

const items = [
  {
    name: 'Black shirt ov doom',
    bandname: 'Doomboyz',
    type: 'Shirt',
    image: 'https://f4.bcbits.com/img/0023801518_10.jpg',
  },
  {
    name: 'Silly tapez',
    bandname: 'Goplord',
    type: 'Cassette',
    image: 'https://f4.bcbits.com/img/0022185148_10.jpg',
  },
]

function MerchItem(props) {
  const itemDisplay = (
      <div>
        <span>{props.name}</span>
        <span>{props.bandname}</span>
        <span>{props.type}</span>
        <img src={props.image}/>
      </div>
  )
  return (
      <Card width='medium' pad={null} background='light-1' key={[props.name, props.bandname]}>
        <Stack
            anchor='bottom-left'
        >
          <CardBody pad={null}>
            <Image
                fit='cover'
                src={props.image}>
            </Image>
          </CardBody>
          <CardFooter
              pad='small'
              justify='start'
              background='#00000080'
              width='medium'
          >
            {props.name}
          </CardFooter>
        </Stack>
        {/*<CardHeader pad='small'>Header</CardHeader>*/}

        {/*<CardFooter pad='small'>Footer</CardFooter>*/}
        {/*{itemDisplay}*/}
      </Card>
  )
}

function MerchGrid(props) {
  return (
      <ResponsiveContext.Consumer>
        {size => (
            <Grid
              rows=''
              columns={size !== 'small' ? 'medium' : '100%'}
              gap='small'
            >
              {props.merchData.map(MerchItem)}
            </Grid>
        )}
      </ResponsiveContext.Consumer>
  )
}

function App() {
  const [merchData, setMerchData] = useState(items);
  return (
      <Grommet theme={theme} background='light-3' full>
        <div className="App">
          <Box>
            <MerchGrid
              merchData={merchData}
              onClick={() => {
                console.log('ooo')
                const i = items.slice();
                i[0].name = 'ok';
                setMerchData(i);
              }}
            />
          </Box>
        </div>
      </Grommet>
  );
}

export default App;
