# Key packages for Dash Web App
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# Data manipulation and validation/formatting
import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import time
import random
import numpy as np
import time

###### Setup ######

# Reads IMGR data from excel file
df = pd.read_excel('IMGR1.xlsx')

# Adds base CUSIP to data frame
df['CUSIP6'] = df['CUSIP'].str[0:6]

# list of ratings for PM to choose from
ratings = [
    'AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-', 'BB+',
    'BB', 'BB-', 'B+', 'B', 'B-', 'CCC+', 'CCC', 'CCC-', 'CC', 'C', 'D'
]

# list comprehension to get all years from currrent to 50 in the future
# incremented by 1 year
years = [dt.now().year + i for i in range(51)]

# simple yes/no list option for PM choice
opt = ['Yes', 'No']

# list of sectors for PM to choose from for bonds. Non-exhaustive
sector = [
    'Water', 'Nursing Homes', 'Education', 'Medical', 'School District',
    'Utilities', 'Pollution', 'General Obligation', 'Transportation',
    'Single Family Housing', 'Airport', 'Multifamily Housing'
]

# list comprehesion to create coupon range, from 1 to 10 in this case
coupon = [i for i in range(1,11)]


# dictionary of rating to number conversion for easy comparison
wells = {
    'AAA':1, 'AA+':2, 'AA':3, 'AA-':4, 'A+':5, 'A':6, 'A-':7, 'BBB+':8, 'BBB':9,
    'BBB-':10}

# list of states for PM to include/exclude
states = [
    'Alabama - AL', 'Alaska - AK', 'Arizona - AZ', 'Arkansas - AR',
    'California - CA', 'Colorado - CO', 'Connecticut - CT',
    'Delaware - DE', 'Florida - FL', 'Georgia - GA', 'Hawaii - HI',
    'Idaho - ID', 'Illinois - IL', 'Indiana - IN', 'Iowa - IA', 'Kansas - KS',
    'Kentucky - KY', 'Louisiana - LA', 'Maine - ME', 'Maryland - MD',
    'Massachusetts - MA', 'Michigan - MI', 'Minnesota - MN', 'Mississippi - MS',
    'Missouri - MO', 'Montana - MT', 'Nebraska - NE', 'Nevada - NV',
    'New Hampshire - NH', 'New Jersey - NJ', 'New Mexico - NM', 'New York - NY',
    'North Carolina - NC', 'North Dakota - ND', 'Ohio - OH', 'Oklahoma - OK',
    'Oregon - OR', 'Pennsylvania - PA', 'Rhode Island - RI',
    'South Carolina - SC', 'South Dakota - SD', 'Tennessee - TN', 'Texas - TX',
    'Utah - UT', 'Vermont - VT', 'Virginia - VA', 'Washington - WA',
    'West Virginia - WV', 'Wisconsin - WI', 'Wyoming - WY', 'American Samoa - AS',
    'District of Columbia - DC', 'Federated States of Micronesia - FM',
    'Guam - GU', 'Marshall Islands - MH', 'Northern Mariana Islands - MP',
    'Palau - PW', 'Puerto Rico - PR', 'Virgin Islands - VI'
]

# alternate list of states/territories
usa = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI",
          "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN",
          "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
          "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX",  "UT", "VT", "VA", "WA",
          "WV", "WI", "WY",
          "AS", "GU", "MP", "PR", "VI", "UM", "FM", "FH", "PW"]

# Dictionary to convert rating to number for comparison
rating = {'AAA':1, 'AA1':2, 'AA2':3, 'AA3':4, 'A1':5, 'A2':6, 'A3':7, 'BAA1':8,
        'BAA2':9, 'BAA3':10, 'BA1':11, 'BA2':12, 'BA3':13, 'B1':14, 'B2':15,
        'B3':16, 'AA+':2, 'AA':3, 'AA-':4, 'A+':5, 'A':6, 'A-':7, 'BBB+':8,
        'BBB':9, 'BBB-':10, 'BB+':11, 'BB':12, 'BB-':13, 'B+':14, 'B':15,
        'B-':16
        }

# reverse dictionary to reconvert to rating
moodyNum = {1:'AAA',2:'AA1',3:'AA2',4:'AA3',5:'A1',6:'A2',7:'A3',8:'BAA1',9:'BAA2',
            10:'BAA3',11:'BA1',12:'BA2',13:'BA3',14:'B1',15:'B2',16:'B3',17:'CAA1',
            18:'CAA2',19:'CAA3',20:'CA',21:'C'
            }

# list of columns to display to trader
col_names = [
        'CUSIP', 'CUSIP6', 'State', 'Coupon', 'Maturity', 'Ask Price', 'Ask Yield To Worst',
        'Ask Size', 'Underlying Moody\'s Rating', 'Call Date', 'Issue Type',
        'Ask Dealer', 'Ask Source'
        ]

# list of columns to display comment in nice format
comment_names = [
    'Increment', 'Size ($)', 'General Market (Y/N)', 'State (include)', 'State (exclude)',
    'Coupon Min (%)', 'Coupon Max (%)', 'Maturity Min', 'Maturity Max',
    'Call', 'Rating Min', 'Rating Max', 'Settle Date After'
]

# External formatting to make site look nice
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# main function that allows the dataframe to update based on comment
def update_data(comment, dataframe):
    # creates copy of dataframe to prevent filter from deleting original data
    dataframe = dataframe[
        [col for col in col_names]].copy()
    # converts maturity to datetime object for date comparision
    dataframe['Maturity'] = pd.to_datetime(dataframe['Maturity']).copy()
    # if call date not specified, returns future call date of 150 years in the future
    dataframe['Call Date'] = dataframe['Call Date'].apply(lambda x: x if x != '#N/A Field Not Applicable' else dt.today() + relativedelta(years = 150)).copy()
    # converts call date to datetime object for date comparision
    dataframe['Call Date'] = pd.to_datetime(dataframe['Call Date']).copy()

    # replace WR (wasn't rated) to NA value for Moody rating
    dataframe['Underlying Moody\'s Rating'].replace('WR', np.nan, inplace = True)
    # removes all rows that don't have Moody's rating since traders don't look at those
    dataframe = dataframe.loc[dataframe['Underlying Moody\'s Rating'].notnull()]
    # converts rating to all upper case to match dictionary
    dataframe['Underlying Moody\'s Rating'] = dataframe['Underlying Moody\'s Rating'].str.upper()
    # converts rating to number
    dataframe['Underlying Moody\'s Rating'].replace(rating, inplace = True)
    # converts number rating to integer type for comparision
    dataframe['Underlying Moody\'s Rating'] = dataframe['Underlying Moody\'s Rating'].astype(int)

    # returns data if blank comment input
    if comment == None or comment == '':
        # converts future no call dates back into not callable format or nice date format for ease of understanding for trader
        dataframe['Call Date'] = dataframe['Call Date'].apply(lambda x: dt.strftime(x, '%m/%d/%Y') if x.year != dt.today().year + 150 else "Not Callable")
        # converts maturity to nice date format that is more easily readable
        dataframe['Maturity'] = dataframe['Maturity'].apply(lambda x: dt.strftime(x, '%m/%d/%Y'))
        # converts number back to rating for trader to view
        dataframe['Underlying Moody\'s Rating'].replace(moodyNum, inplace=True)
        # returns data to data table
        return dataframe.to_dict('records')
    else:
        # split comment from template based on comma delimiter
        lst = comment.split(',')

        # muli state handling

        # get indices of start and end of each list
        start = [i for i, char in enumerate(lst) if '[' in char]
        end = [i+1 for i, char in enumerate(lst) if ']' in char]
        # if only mulit in either include or exlude state
        if len(start) == 1:
            lst[start[0]:end[0]] = [''.join(lst[start[0]:end[0]])]
        # if both include and exclude have multi state
        elif len(start) == 2:
            lst[start[0]:end[0]] = [''.join(lst[start[0]:end[0]])]
            start = [i for i, char in enumerate(lst) if '[' in char]
            end = [i+1 for i, char in enumerate(lst) if ']' in char]
            lst[start[1]:end[1]] = [''.join(lst[start[1]:end[1]])]
        print(lst)
        # convert string to list
        lst[3] = lst[3].replace("'", '')
        lst[4] = lst[4].replace("'", '')
        lst[3] = lst[3].strip('][').split(' ')
        lst[4] = lst[4].strip('][').split(' ')

        print(lst)
        #Set defaults for empty string/no input from template

        # default for coupon min is 1
        if lst[5] == '':
            lst[5] = 1
        else:
            lst[5] = float(lst[5])

        # default for coupon max is 10
        if lst[6] == '':
            lst[6] = 10
        else:
            lst[6] = float(lst[6])

        # default for maturity min is current year
        if lst[7] == '':
            lst[7] = dt.now()
        else:
            lst[7] = dt.strptime(lst[7], '%Y')

        # default for maturity max is 50 years in the future
        if lst[8] == '':
            lst[8] = dt.now() + relativedelta(years = 50)
        else:
            lst[8] = dt.strptime(lst[8] + ' 12 31', '%Y %m %d')
        
        # default for call date is current year
        if lst[9] == '':
            lst[9] = dt.now()
        else:
            lst[9] = dt.strptime(lst[9], '%Y')
        
        # default for rating min is investment grade
        if lst[10] == '':
            lst[10] = 16
        else:
            lst[10] = rating[lst[10].upper()]
        
        # default for rating max is AAA
        if lst[11] == '':
            lst[11] = 1
        else:
            lst[11] = rating[lst[11].upper()]

        # if state preferred is not specified, return general market minus
        # state to exclude
        if lst[3][0] == '':
            dataframe = dataframe[(dataframe['Ask Size'] >= float(lst[1])) &
                                  (~dataframe['State'].isin(lst[4])) &
                                  (dataframe['Coupon'] >= lst[5]) &
                                  (dataframe['Coupon'] <= lst[6]) &
                                  (dataframe['Maturity'] >= lst[7]) &
                                  (dataframe['Maturity'] <= lst[8]) &
                                  (dataframe['Call Date'] >= lst[9]) &
                                  (dataframe['Underlying Moody\'s Rating'] <= lst[10]) &
                                  (dataframe['Underlying Moody\'s Rating'] >= lst[11])]
            # converts call date back into not callable from 150 years in the future or nice date format
            dataframe['Call Date'] = dataframe['Call Date'].apply(lambda x: dt.strftime(x, '%m/%d/%Y') if x.year != dt.today().year + 150 else "Not Callable")
            # converts maturity to nice date format
            dataframe['Maturity'] = dataframe['Maturity'].apply(lambda x: dt.strftime(x, '%m/%d/%Y'))
            # converts number back into rating
            dataframe['Underlying Moody\'s Rating'].replace(moodyNum, inplace=True)
            return dataframe.to_dict('records')
        
        # if preferred state and general market is yes, return matching results
        elif lst[2] == 'Yes':
            dataframe1 = dataframe[(dataframe['Ask Size'] >= float(lst[1])) &
                                  (dataframe['State'].isin(lst[3])) &
                                  (~dataframe['State'].isin(lst[4])) &
                                  (dataframe['Coupon'] >= lst[5]) &
                                  (dataframe['Coupon'] <= lst[6]) &
                                  (dataframe['Maturity'] >= lst[7]) &
                                  (dataframe['Maturity'] <= lst[8]) &
                                  (dataframe['Call Date'] >= lst[9]) &
                                  (dataframe['Underlying Moody\'s Rating'] <= lst[10]) &
                                  (dataframe['Underlying Moody\'s Rating'] >= lst[11])]
            dataframe2 = dataframe[(dataframe['Ask Size'] >= float(lst[1])) &
                                #   (dataframe['State'].isin(lst[3])) &
                                  (~dataframe['State'].isin(lst[4])) &
                                  (dataframe['Coupon'] >= lst[5]) &
                                  (dataframe['Coupon'] <= lst[6]) &
                                  (dataframe['Maturity'] >= lst[7]) &
                                  (dataframe['Maturity'] <= lst[8]) &
                                  (dataframe['Call Date'] >= lst[9]) &
                                  (dataframe['Underlying Moody\'s Rating'] <= lst[10]) &
                                  (dataframe['Underlying Moody\'s Rating'] >= lst[11])]

            dataframe1 = dataframe1.append(dataframe2, ignore_index=True)

            dataframe1['Call Date'] = dataframe1['Call Date'].apply(lambda x: dt.strftime(x, '%m/%d/%Y') if x.year != dt.today().year + 150 else "Not Callable")
            dataframe1['Maturity'] = dataframe1['Maturity'].apply(lambda x: dt.strftime(x, '%m/%d/%Y'))
            dataframe1['Underlying Moody\'s Rating'].replace(moodyNum, inplace=True)
            return dataframe1.to_dict('records')
        # if no general allowed, include only preferred state
        else:
            dataframe = dataframe[(dataframe['State'].isin(lst[3])) &
                                  (dataframe['Ask Size'] >= float(lst[1])) &
                                  (~dataframe['State'].isin(lst[4])) &
                                  (dataframe['Coupon'] >= lst[5]) &
                                  (dataframe['Coupon'] <= lst[6]) &
                                  (dataframe['Maturity'] >= lst[7]) &
                                  (dataframe['Maturity'] <= lst[8]) &
                                  (dataframe['Call Date'] >= lst[9]) &
                                  (dataframe['Underlying Moody\'s Rating'] <= lst[10]) &
                                  (dataframe['Underlying Moody\'s Rating'] >= lst[11])]

            dataframe['Call Date'] = dataframe['Call Date'].apply(lambda x: dt.strftime(x, '%m/%d/%Y') if x.year != dt.today().year + 150 else "Not Callable")
            dataframe['Maturity'] = dataframe['Maturity'].apply(lambda x: dt.strftime(x, '%m/%d/%Y'))
            dataframe['Underlying Moody\'s Rating'].replace(moodyNum, inplace=True)
            return dataframe.to_dict('records')

























# Beginning of web interface that is displayed by web browser

app.layout = html.Div(children=[
    # title of page
    html.H4('IMGR Dashboard'),

    # Comment input and manager comment display
    # Submit button to convert comment to explanatory table
    html.Div(children = [
        html.Label('Comment',
                style={'grid-row':'1 / 2', 'grid-column':'1 / 2'}),

        dcc.Input(
                'ScreenName_Input',
                type='text',
                style={'grid-row':'2 / 3', 'grid-column':'1 / 2', 'width': '600%'}
                ),
        dcc.Input(
                id='manager',
                disabled=True,
                value='',
                style={'grid-row':'4 / 6', 'grid-column':'1 / 2', 'width': '600%'}
            ),
        html.Button(
                id='submit',
                children='Submit',
                n_clicks=0,
                style={'grid-row':'2 / 3', 'grid-column':'7 / 9', 'width': '100%'}
                ),
    ],
        # CSS style to display on web page nicely
        style={'display':'grid', 'grid-template-rows':'25px 25px 25px 25px',
               'grid-auto-columns': '100px 100px 100px 100px 150px'}
    ),
    # Break element for spacing between elements of page
    html.Br(),
    # Explantory table to remind trader what comment represents
    # Allows trader to make adjustments to find a bond if comment is too restrictive
    html.Div(children=[
        html.Table(
            [html.Tr([
                html.Th(col)
                for col in comment_names
            ])] +

            [html.Tr(
                [
                    html.Td(
                        dcc.Input(
                            id='increment',
                            placeholder='Input Increment',
                            value='',
                            type='number',
                            min=1,
                            max=50,
                            step=1,
                            style={'width':60}
                        )
                    ),

                    html.Td(
                        dcc.Input(
                            id='size',
                            value='',
                            placeholder='Input Size',
                            min=10000,
                            max=1000000000,
                            step=1,
                            style={'width':80}
                        )
                    ),

                    html.Td(
                        dcc.Dropdown(
                            id='general',
                            options=[
                                {'label':o, 'value':o}
                                for o in opt
                            ],
                            value='',
                            placeholder='Allow General Market?',
                            style={'width':100}
                        )
                    ),

                    html.Td(
                        dcc.Dropdown(
                            id='stateIncl',
                            options=[
                                {'label':s, 'value':s}
                                for s in usa
                            ],
                            value='',
                            placeholder='Select State',
                            multi=True,
                            style={'width':100}
                        )
                    ),

                    html.Td(
                        dcc.Dropdown(
                            id='stateExcl',
                            # options=[
                            #     {'label':s, 'value':s}
                            #     for s in states
                            # ],
                            value='',
                            placeholder='Select State',
                            multi=True,
                            style={'width':100}
                        )
                    ),

                    html.Td(
                        dcc.Dropdown(
                            id='couponMin',
                            options=[
                                {'label':c, 'value':c}
                                for c in coupon
                            ],
                            value='',
                            placeholder='Select Rating',
                            style={'width':100}
                        ),
                    ),

                    html.Td(
                        dcc.Dropdown(
                            id='couponMax',
                            # options=[
                            #     {'label':r, 'value':r}
                            #     for r in wells.keys()
                            # ],
                            value='',
                            placeholder='Select Rating',
                            style={'width':100}
                        ),
                    ),

                    html.Td(
                        dcc.Dropdown(
                            id='maturityMin',
                            options=[
                                {'label':d, 'value':d}
                                for d in years
                            ],
                            value='',
                            placeholder='Select Maturity',
                            style={'width':100}
                        ),
                    ),

                    html.Td(
                        dcc.Dropdown(
                            id='maturityMax',
                            # options=[
                            #     {'label':r, 'value':r}
                            #     for r in wells.keys()
                            # ],
                            value='',
                            placeholder='Select Maturity',
                            style={'width':100}
                        ),
                    ),

                    html.Td(
                        dcc.Dropdown(
                            id='call',
                            options=[
                                {'label':d, 'value':d}
                                for d in years
                            ],
                            value='',
                            placeholder='Call Date',
                            style={'width': 100,
                                    'margin':'auto'}
                        )
                    ),

                    html.Td(
                        dcc.Dropdown(
                            id='ratingMin',
                            options=[
                                {'label':r, 'value':r}
                                for r in wells.keys()
                            ],
                            value='',
                            placeholder='Select Rating',
                            style={'width':100}
                        ),
                    ),

                    html.Td(
                        dcc.Dropdown(
                            id='ratingMax',
                            # options=[
                            #     {'label':r, 'value':r}
                            #     for r in ratings
                            # ],
                            placeholder='Select Rating',
                            value='',
                            style={'width':100}
                        ),
                    ),

                    html.Td(
                        dcc.DatePickerSingle(
                            id='settledate',
                            month_format='MMMM Y',
                            placeholder='MMMM Y',
                            date=dt.today(),
                            min_date_allowed=dt.today(),
                            max_date_allowed=dt.now() + relativedelta(years=50),
                            style={'width':100}
                            # with_full_screen_portal=True
                        )
                    )
                ]
            )]
        , style = {'grid-row':'3 / 8', 'width':'10px'}),

        ],

    ),

    # button to refilter data from explanatory table
    html.Button(
        "Refilter",
        id='filter',
        n_clicks=0
    ),
    # more breaks for spacing
    html.Br(),
    html.Br(),
    html.Br(),

    # display of filtered IMGR data
    html.Div(children=[
            dash_table.DataTable(
            id='IMGR_table',
            columns=[
                    {'name': c, 'id': c}
                    for c in col_names
                    ],
            # Allows filtering/sorting of data table
            filter_action='native',
            sort_action='native',
            sort_mode='multi',
            # Restricts showing 25 results per page
            page_action='native',
            page_size=25
            ),

    ],
        style={'display':'grid', 'grid-template-columns': '1fr 1fr',
                'column-gap':'10px', 'margin-top':'-25px'}
        ),

])


###### Callbacks ######


# call back that resets button click count when button is clicked
# prevents constant dynamic updating that slows down app
@app.callback(
    [Output('submit', 'n_clicks'),
    Output('filter', 'n_clicks')],
    [Input('filter', 'n_clicks_timestamp'),
    Input('submit', 'n_clicks_timestamp')]
)
def resetClicks(value, stamp):
    time.sleep(1)
    return 0, 0

# takes comment and displays into explantory table
@app.callback(
    [Output('increment', 'value'),
    Output('size', 'value'),
    Output('general', 'value'),
    Output('stateIncl', 'value'),
    Output('stateExcl', 'value'),
    Output('couponMin', 'value'),
    Output('couponMax', 'value'),
    # Output('price', 'value'),
    # Output('yield', 'value'),
    Output('maturityMin', 'value'),
    Output('maturityMax', 'value'),
    Output('call', 'value'),
    Output('ratingMin', 'value'),
    Output('ratingMax', 'value'),
    # Output('accrued', 'value'),
    Output('settledate', 'date'),
    # Output('sector', 'value'),
    Output('manager', 'value')
    ],
    [Input('submit', 'n_clicks'),
    Input('ScreenName_Input', 'value')]
)
def help(n_clicks, comment):
    # if comment is empty, return all data
    if (n_clicks > 0 and comment != None and comment != ''):
        l = comment.split(',')
        if len(l[3]) > 2:
            l[3] = l[3].split(' ')
        if len(l[4]) > 2:
            l[4] = l[4].split(' ')
        return l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8], l[9], l[10], l[11], l[12], l[13]
    # if comment is pasted, display comment in explanatory table
    elif(n_clicks > 0 and (comment == None or comment == '')):
        return '', '', '', '', '', '', '', '', '', '', '', '', dt.now(), '',
    # prevents background updates if comment is not correctly formatted
    # also keeps updates from constantly happening on start of app
    else:
        raise PreventUpdate


# takes fields from explanatory table and filters based on fields
@app.callback(
    Output('IMGR_table', 'data'),
    # Output('IMGR_table', 'data'),
    [   Input('filter', 'n_clicks'),
        Input('increment', 'value'),
        Input('size', 'value'),
        Input('general', 'value'),
        Input('stateIncl', 'value'),
        Input('stateExcl', 'value'),
        Input('couponMin', 'value'),
        Input('couponMax', 'value'),
        # Input('price', 'value'),
        # Input('yield', 'value'),
        Input('maturityMin', 'value'),
        Input('maturityMax', 'value'),
        Input('call', 'value'),
        Input('ratingMin', 'value'),
        Input('ratingMax', 'value'),
        # Input('accrued', 'value'),
        Input('settledate', 'date'),
        # Input('sector', 'value'),
        Input('manager', 'value')
    ]
)
def dynamic(n_clicks, increment, size, general, stateIncl, stateExcl, couponMin, couponMax,
            maturityMin, maturityMax, call, ratingMin, ratingMax, settledate, manager):
    # catch empty fields and converts to empty string
    if(increment == None):
        increment = ''
    if(size == None):
        size = ''
    if(general == None):
        general = ''
    if(stateIncl == None):
        stateIncl = ''
    if(stateExcl == None):
        stateExcl = ''
    if(couponMin == None):
        couponMin = ''
    if(couponMax == None):
        couponMax = ''
    if(maturityMin == None):
        maturityMin = ''
    if(maturityMax == None):
        maturityMax = ''
    if(call == None):
        call = ''
    if(ratingMin == None):
        ratingMin = ''
    if(ratingMax == None):
        ratingMax = ''
    if(settledate == None):
        settledate = dt.now()
    if(manager == None):
        manager = ''
    # rebuilds new comment string in same format
    comment = (str(increment) + ',' + str(size) + ',' + str(general) + ',' +
            str(stateIncl) + ',' + str(stateExcl) + ',' + str(couponMin) + ',' +
            str(couponMax) + ',' + str(maturityMin) + ',' + str(maturityMax) + ',' +
            str(call) + ',' + str(ratingMin) + ',' + str(ratingMax) + ',' +
            str(settledate) + ',' + str(manager)
                )
    # checks validity of comment
    if(n_clicks > 0 and str(increment) != '' and str(size) != '' and str(general) != ''):
        return update_data(comment, df)
    # if blank comment, return all results
    elif(n_clicks > 0 and str(increment) == '' and str(size) == '' and str(general) == ''):
        return update_data('', df)
    # update prevention to speed up app
    else:
        raise PreventUpdate


# Callback to restrict ratingMin range from ratingMax value
@app.callback(
    Output('ratingMin', 'options'),
    [Input('ratingMax', 'value')]
)
def setRatingMin(rating):
    if(rating == None or rating == ''):
        return [
            {'label':r, 'value':r}
            for r in wells.keys()
        ]
    else:
        return [
            {'label':r, 'value':r}
            for r in wells.keys() if wells[r] >= wells[rating]
        ]

# callback to restrict ratingMax range from ratingMin value
@app.callback(
    Output('ratingMax', 'options'),
    [Input('ratingMin', 'value')]
)
def setRatingMax(rating):
    if(rating == None or rating == ''):
        return [
            {'label':r, 'value':r}
            for r in wells.keys()
        ]
    else:
        return [
            {'label':r, 'value':r}
            for r in wells.keys() if wells[r] <= wells[rating]
        ]

# callback to restrict maturityMin range from maturityMax value
@app.callback(
    Output('maturityMin', 'options'),
    [Input('maturityMax', 'value')]
)
def setMaturityMin(year):
    try:
        year = int(year)
    except:
        year = year
    if(year == None or year == ''):
        return [
            {'label':d, 'value':d}
            for d in years
        ]
    else:
        return [
            {'label':d, 'value':d}
            for d in years if d <= year
        ]

# callback to restrict maturityMax range from maturityMin value
@app.callback(
    Output('maturityMax', 'options'),
    [Input('maturityMin', 'value')]
)
def setMaturityMax(year):
    try:
        year = int(year)
    except:
        year = year
    if(year == None or year == ''):
        return [
            {'label':d, 'value':d}
            for d in years
        ]
    else:
        return [
            {'label':d, 'value':d}
            for d in years if d >= year
        ]

# callback to restrict couponMin range from couponMax value
@app.callback(
    Output('couponMin', 'options'),
    [Input('couponMax', 'value')]
)
def setMaturityMin(cpn):
    try:
        cpn = int(cpn)
    except:
        cpn = cpn
    if(cpn == None or cpn == ''):
        return [
            {'label':c, 'value':c}
            for c in coupon
        ]
    else:
        return [
            {'label':c, 'value':c}
            for c in coupon if c <= cpn
        ]

# callback to restrict couponMax range from couponMin value
@app.callback(
    Output('couponMax', 'options'),
    [Input('couponMin', 'value')]
)
def setMaturityMax(cpn):
    try:
        cpn = int(cpn)
    except:
        cpn = cpn
    if(cpn == None or cpn == ''):
        return [
            {'label':c, 'value':c}
            for c in coupon
        ]
    else:
        return [
            {'label':c, 'value':c}
            for c in coupon if c >= cpn
        ]

# callback to restrict stateExcl range from stateIncl value
@app.callback(
    Output('stateExcl', 'options'),
    [Input('stateIncl', 'value')]
)
def setStateExcl(state):
    if(state == None or state == ''):
        return [
            {'label': s, 'value': s}
            for s in usa
        ]
    else:
        return [
            {'label':s, 'value':s}
            for s in usa if s not in state
        ]

# callback to restrict stateIncl range from stateExcl value
@app.callback(
    Output('stateIncl', 'options'),
    [Input('stateExcl', 'value')]
)
def setStateExcl(state):
    if(state == None or state == ''):
        return [
            {'label': s, 'value': s}
            for s in usa
        ]
    else:
        return [
            {'label':s, 'value':s}
            for s in usa if s not in state
        ]






if __name__ == '__main__':
    app.run_server(debug=False, port = 8051)
#    webbrowser.open_new('http://127.0.0.1:8050/')
