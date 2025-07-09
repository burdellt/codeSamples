import pandas as pd

def message_decoder(gsheet,gid) :
    ##import data
    url = f'https://docs.google.com/spreadsheets/d/{gsheet}/export?format=csv&gid={gid}'
    df = pd.read_csv(url)

    ##find min and max coordinate values
    ymax = int(df['y-coordinate'].max())    
    ymin = int(df['y-coordinate'].min())
    xmax = int(df['x-coordinate'].max())
    xmin = int(df['x-coordinate'].min())

    ##Create a grid using the x, y coordinates and leaving a empty value for the character
    grid = [[' ' for _ in range(xmax + 1)] for _ in range(ymax + 1)]
   
    ## Assign Characters to corresponding grid coordinates
    for x, y, char in df[['x-coordinate','y-coordinate','Character' ]].values:
        grid[y][x] = char

    ## Smash it together!
    for row in grid:
        print(''.join(row))

message_decoder('16PfFAB2gNEwv577yWY2ukojKnltDdFFqmdBU8fH7cCw',740427962)