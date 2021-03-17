import React, {useContext} from 'react';
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

// class MerchGrid extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       cells: Array(props.numCells).fill('testCell'),
//     }
//   }
//
//   renderCell(i) {
//     return (
//         <Cell msg={i}>
//           {this.state.cells[i]}
//         </Cell>
//     )
//   }
//
//   render() {
//     const cells = this.state.cells.slice()
//     // const testcells =
//     return (
//         <div>
//           {this.renderCell(0)}
//         </div>
//     )
//   }
// }
//
// function Cell(props) {
//   return (
//       <li>{props.msg}</li>
//   )
// }

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


class MerchGrid extends React.Component {
  constructor(props) {
    super(props);
  }

  renderItem(item, index) {
    const itemDisplay = (
        <div>
          <span>{item.name}</span>
          <span>{item.bandname}</span>
          <span>{item.type}</span>
          <img src={item.image}/>
        </div>
    )
    return (
      <Card width='medium' pad={null} background='light-1' key={[item.name, item.bandname]}>
        <Stack
            anchor='bottom-left'
          >
          <CardBody pad={null}>
            <Image
                fit='cover'
                src={item.image}>
            </Image>
          </CardBody>
          <CardFooter
              pad='small'
              justify='start'
              background='#00000080'
              width='medium'
          >
            {item.name}
          </CardFooter>
        </Stack>
        {/*<CardHeader pad='small'>Header</CardHeader>*/}

        {/*<CardFooter pad='small'>Footer</CardFooter>*/}
        {/*{itemDisplay}*/}
      </Card>
    )
  }

  render() {
    const merchItems = Array(10).fill('sample');
    return (
        <ResponsiveContext.Consumer>
          {size => (
              <Grid
                rows=''
                columns={size !== 'small' ? 'medium' : '100%'}
                gap='small'
              >
                {items.map(this.renderItem)}
              </Grid>
              // <Grid
              //     columns
              // >
              //   <Box gridArea='header' background='brand'/>
              //   <Box gridArea='nav' background='light-5'/>
              //   <Box gridArea='main' background='light-2'/>
              // </Grid>
          )}
        </ResponsiveContext.Consumer>
    )
  }
}

function App() {
  return (
      <Grommet theme={theme} background='light-3' full>
        <div className="App">
          <Box>
            <MerchGrid/>
          </Box>
        </div>
      </Grommet>
  );
}

export default App;
