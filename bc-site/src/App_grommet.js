import { Box, Button, Collapsible, Heading, Grommet, Layer, ResponsiveContext } from 'grommet';
import { Notification } from 'grommet-icons';
import React, { useState } from 'react';

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

function AppBar(props) {
  return (
      <Box
          tag='header'
          direction='row'
          align='center'
          justify='between'
          background='brand'
          pad={{left: 'medium', right: 'small', vertical: 'small'}}
          elevation='medium'
          style={{zIndex: '1'}}
          {...props}
      />
  )
}

function App() {
    const [showSidebar, setShowSidebar] = useState(false);
    return (
        <Grommet theme={theme} full>
            <ResponsiveContext.Consumer>
                {size => (
                    <Box fill>
                        <AppBar>
                            <Heading level='3' margin='none'>My App</Heading>
                            <Button
                                icon={<Notification />}
                                onClick={() => setShowSidebar(!showSidebar)} />
                        </AppBar>
                        <Box direction='row' flex overflow={{horizontal: 'hidden'}}>
                            <Box flex align='center' justify='center'>
                                app body
                            </Box>
                            {(!showSidebar || size !== 'small') ? (
                                <Collapsible direction='horizontal' open={showSidebar}>
                                    <Box
                                        flex
                                        width='medium'
                                        background='light-2'
                                        elevation='small'
                                        align='center'
                                        justify='center'
                                    >
                                        sidebar
                                    </Box>
                                </Collapsible>
                            ): (
                                <Layer>
                                    <Box
                                        fill
                                        background='light-2'
                                        align='center'
                                        justify='center'
                                    >
                                        sidebar
                                    </Box>
                                </Layer>
                            )}
                        </Box>
                    </Box>
                )}
            </ResponsiveContext.Consumer>
        </Grommet>
    );
}

export default App;
