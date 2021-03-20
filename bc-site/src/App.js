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

function MerchItem({name, bandname, type, image}) {
  // const itemDisplay = (
  //     <div>
  //       <span>{name}</span>
  //       <span>{bandname}</span>
  //       <span>{type}</span>
  //       <img src={image}/>
  //     </div>
  // )
  return (
      <Card width='medium' pad={null} background='light-1' key={[name, bandname]}>
        <Stack
            anchor='bottom-left'
        >
          <CardBody pad={null}>
            <Image
                fit='cover'
                src={image}>
            </Image>
          </CardBody>
          <CardFooter
              pad='small'
              justify='start'
              background='#00000080'
              width='medium'
          >
            {name}
          </CardFooter>
        </Stack>
        {/*<CardHeader pad='small'>Header</CardHeader>*/}

        {/*<CardFooter pad='small'>Footer</CardFooter>*/}
        {/*{itemDisplay}*/}
      </Card>
  )
}

function MerchGrid({merchData}) {
  return (
      <ResponsiveContext.Consumer>
        {size => (
            <Grid
              rows=''
              columns={size !== 'small' ? 'medium' : '100%'}
              gap='small'
            >
              {merchData
                .map(({
                        name, bandname, type, image
                      }) => {
                  return (
                    <MerchItem
                      name={name}
                      bandname={bandname}
                      type={type}
                      image={image}
                    />
                  );
                })}
            </Grid>
        )}
      </ResponsiveContext.Consumer>
  );
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
