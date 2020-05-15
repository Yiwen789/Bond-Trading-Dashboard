import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import dash_table.FormatTemplate as FormatTemplate
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# list of ratings for PM to choose from
ratings = [
    'AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-', 'BB+', 
    'BB', 'BB-', 'B+', 'B', 'B-', 'CCC+', 'CCC', 'CCC-', 'CC', 'C', 'D'
]

# list comprehension to get all years from currrent to 50 in the future
# incremented by 1 year
years = [datetime.now().year + i for i in range(51)]

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
    
#     , 'BB+':11, 'BB':12, 'BB-':13, 'B+':14, 'B':15, 'B-':16, 'CCC+':17,
#     'CCC':18, 'CCC-':19, 'CC':20, 'C':21, 'D':22
# }


# col_names = [
#     'Increment', 'Size ($)', 'General Market (Y/N)', 'State (include)', 'State (exclude)',
#     'Coupon Min (%)', 'Coupon Max (%)',  'Price ($)', 'Yield (%)', 'Maturity Min', 'Maturity Max',
#     'Call', 'Rating Min', 'Rating Max', 'Accrued Interest (Y/N)', 'Settle Date After', 'Sector'
# ]

# Column names for PM to change
col_names = [
    'Increment', 'Size ($)', 'General Market (Y/N)', 'State (include)', 'State (exclude)',
    'Coupon Min (%)', 'Coupon Max (%)', 'Maturity Min', 'Maturity Max',
    'Call', 'Rating Min', 'Rating Max', 'Settle Date After'
]

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

# dictionary comprehension to shorten state abbreviation
shorthand = {x:y for x,y in zip(states, usa)}
shorthand[''] = ''

# Dash Web Layout Creator
app = dash.Dash(__name__)
# Browser tab title
app.title="TESTING"

# Start of Dash HTML Loading
app.layout = html.Div([
    # Description of template table
    # HTML Table tag
    html.Table(
        # TR = Table Row, creates title that spans two columns
        [html.Tr(
            html.Th("HELP", colSpan='2')
        )] +
        # TR for each variable
        [html.Tr(
            [
                html.Td(
                    "Increment"
                ),

                html.Td(
                    ("Count of sizes to buy. MUST BE INCLUDED.")
                    
                )
            ]
        )] +

        [html.Tr(
            [
                html.Td(
                    "Size"
                ),

                html.Td(
                    ("Dollar Amount of bonds to buy (min $10k)."
                    " MUST BE INCLUDED.")
                    
                )
            ]
        )] +

        [html.Tr(
            [
                html.Td(
                    "General Market"
                ),

                html.Td(
                    ("Allow bonds from the general market? (Y/N)."
                    " MUST BE INCLUDED.")
                    
                )
            ]
        )] +

        [html.Tr(
            [
                html.Td(
                    "State"
                ),

                html.Td(
                    ("States to include/exclude. Optional.")
                    
                )
            ]
        )] +

        [html.Tr(
            [
                html.Td(
                    "Coupon"
                ),

                html.Td(
                    ("Min/Max Coupon (%). Optional.")
                    
                )
            ]
        )] +

        # [html.Tr(
        #     [
        #         html.Td(
        #             "Price"
        #         ),

        #         html.Td(
        #             ("Price of bond. Optional.")
                    
        #         )
        #     ]
        # )] +

        # [html.Tr(
        #     [
        #         html.Td(
        #             "Yield"
        #         ),

        #         html.Td(
        #             ("Percent yield of bond. Optional.")
                    
        #         )
        #     ]
        # )] +

        [html.Tr(
            [
                html.Td(
                    "Maturity"
                ),

                html.Td(
                    ("Future maturity date range (min/max). Optional.")
                    
                )
            ]
        )] +

        [html.Tr(
            [
                html.Td(
                    "Call"
                ),

                html.Td(
                    ("Minimum bond call year. Optional.")
                    
                )
            ]
        )] +

        [html.Tr(
            [
                html.Td(
                    "Rating"
                ),

                html.Td(
                    ("Min/Max Rating of bonds. Optional.")
                    
                )
            ]
        )] +

        # [html.Tr(
        #     [
        #         html.Td(
        #             "Accrued Interest"
        #         ),

        #         html.Td(
        #             ("Allow accrued interest bonds? (Y/N). Optional.")
                    
        #         )
        #     ]
        # )] +

        [html.Tr(
            [
                html.Td(
                    "Settle Date After"
                ),

                html.Td(
                    ("Earliest date when bond can be bought. Optional.")
                    
                )
            ]
        )] +

        # [html.Tr(
        #     [
        #         html.Td(
        #             "Sector"
        #         ),

        #         html.Td(
        #             ("Bond sector type. Optional.")
                    
        #         )
        #     ]
        # )]

        [html.Tr(
            [
                html.Td(
                    "Manager Comment"
                ),

                html.Td(
                    ("Additional information as needed. Optional.")
                    
                )
            ]
        )] 
        
        ,
        className='help'
    ),
    # HTML Line Breaks, for visual separation of HTML elements
    html.Br(),

    html.Br(),

    # Template Table
    html.Table(
        # Header Row
        [html.Tr([html.Th(col) for col in col_names])] +
        # Body Rows for data validation for the PM
        [html.Tr(
            [
                html.Td(
                    # Input field for increment of bonds
                    dcc.Input(
                        id='increment',
                        placeholder='Input Increment',
                        type='number',
                        min=1,
                        max=50,
                        # Step is increment increase, ex: 1 to 2 for step = 1
                        # if step = 2, then the ex would be 1 to 3 to 5...
                        step=1
                    )
                ),

                html.Td(
                    # Input field for size ($) of bonds.
                    dcc.Input(
                        id='size',
                        placeholder='Input Size',
                        type='number',
                        min=10000,
                        max=1000000000,
                        step=1,
                        # Sets size of input box to 60 pixels
                        # Done for visual fit
                        style={'width': 60}
                    )
                ),

                html.Td(
                    dcc.Dropdown(
                        # Yes/No option for general market bonds
                        id='general',
                        # List comprehension for options
                        options=[
                            {'label':o, 'value':o}
                            for o in opt
                        ],
                        value='',
                        placeholder='Allow General Market?'
                    )
                ),

                html.Td(
                    dcc.Dropdown(
                        # States to choose from to include
                        id='stateIncl',
                        # List comprehension for options
                        options=[
                            {'label':s, 'value':s}
                            for s in states
                        ],
                        value='',
                        placeholder='Select State',
                        multi=True
                    )
                ),

                html.Td(
                    dcc.Dropdown(
                        # States to choose from to exclude
                        id='stateExcl',
                        # options=[
                        #     {'label':s, 'value':s}
                        #     for s in states
                        # ],
                        value='',
                        placeholder='Select State',
                        multi=True
                    )
                ),

                html.Td(
                    dcc.Dropdown(
                        # Coupon range
                        id='couponMin',
                        # List comprehension for options
                        options=[
                            {'label':c, 'value':c}
                            for c in coupon
                        ],
                        value='',
                        placeholder='Select Rating'
                    ),
                ),

                html.Td(
                    dcc.Dropdown(
                        # Coupon range
                        id='couponMax',
                        # options=[
                        #     {'label':r, 'value':r}
                        #     for r in wells.keys()
                        # ],
                        value='',
                        placeholder='Select Rating'
                    ),
                ),

                # html.Td(
                #     dcc.Input(
                #         id='price',
                #         type='number',
                #         placeholder='Input Price',
                #         min=95,
                #         max=150,
                #         step=1
                #     )
                # ),

                # html.Td(
                #     dcc.Input(
                #         id='yield',
                #         placeholder='Input Yield',
                #         type='number',
                #         min=0,
                #         max=20,
                #         style={'width': 60}
                #     )
                # ),

                html.Td(
                    dcc.Dropdown(
                        # Maturity range
                        id='maturityMin',
                        # List comprehension for options
                        options=[
                            {'label':d, 'value':d}
                            for d in years
                        ],
                        value='',
                        placeholder='Select Maturity'
                    ),
                ),

                html.Td(
                    dcc.Dropdown(
                        # Maturity range
                        id='maturityMax',
                        # options=[
                        #     {'label':r, 'value':r}
                        #     for r in wells.keys()
                        # ],
                        value='',
                        placeholder='Select Maturity'
                    ),
                ),
                
                html.Td(
                    dcc.Dropdown(
                        # Call date
                        id='call',
                        # List comprehension for options
                        options=[
                            {'label':d, 'value':d}
                            for d in years
                        ],
                        value='',
                        placeholder='Call Date',
                        style={'width': 60,
                                'margin':'auto'}
                    )
                ),

                html.Td(
                    dcc.Dropdown(
                        # Rating range
                        id='ratingMin',
                        # List comprehension for options
                        options=[
                            {'label':r, 'value':r}
                            for r in wells.keys()
                        ],
                        value='',
                        placeholder='Select Rating'
                    ),
                ),

                html.Td(
                    dcc.Dropdown(
                        # Rating range
                        id='ratingMax',
                        # options=[
                        #     {'label':r, 'value':r}
                        #     for r in ratings
                        # ],
                        placeholder='Select Rating'
                    ),
                ),

                # html.Td(
                #     dcc.Dropdown(
                #         id='accrued',
                #         options=[
                #             {'label':o, 'value':o}
                #             for o in opt
                #         ],
                #         value='',
                #         placeholder='Allow Interest?'
                #     )
                # ),

                html.Td(
                    # Settle date
                    dcc.DatePickerSingle(
                        id='settledate',
                        # format of date
                        month_format='MMMM Y',
                        placeholder='MMMM Y',
                        # placeholder date is current date
                        date=datetime.now(),
                        # date is between current year and 50 years in the future
                        min_date_allowed=datetime.now(),
                        max_date_allowed=datetime.now() + relativedelta(years=50)
                        # with_full_screen_portal=True
                    )
                ),

                # html.Td(
                #     dcc.Dropdown(
                #         id='sector',
                #         options=[
                #             {'label':s, 'value':s}
                #             for s in sector
                #         ],
                #         value='',
                #         placeholder='Select Sector',
                #         style={'width': 80}
                #     ),
                # )
            ]
        )] +

        [html.Tr(
            html.Th("Manager Comment", colSpan='13')
        )]+

        [html.Tr(
            [html.Td(
                dcc.Input(
                    # Additional field for PM special instructions
                    id='manager',
                    type='text',
                    placeholder='Input additional information here',
                    value='',
                    style={'width':'95%'}
                ), colSpan='13'
            )]
        )]
    ),

    
    html.Br(),

    html.Button('Add Row', id='editing-rows-button', n_clicks=0),

    html.Br(),
    html.Br(),

    # Output Table
    dash_table.DataTable(
        id='adding-rows-table',
        style_header={
            'whiteSpace':'normal'
        },
        # Dictionary comprehension to create header row for data table
        columns = [ 
            {'id':col, 'name':col}
            for col in col_names
        ] +
        [{'id':'Manager Comment', 'name':'Manager Comment'}]
        ,
        data = [],
        # Allows PM to delete row if info input is incorrect or needs update
        row_deletable=True,
        # Allows PM to export as csv
        export_format='csv',
    ),

])

# Call back to update data table with new standard comment
# Input: button click, data in fields of template
# Output: new row in data table
@app.callback(
    # Id, Property
    Output('adding-rows-table', 'data'),
    [Input('editing-rows-button', 'n_clicks')],
    [
        State('adding-rows-table', 'data'),
        State('adding-rows-table', 'columns'),
        State('increment', 'value'),
        State('size', 'value'),
        State('general', 'value'),
        State('stateIncl', 'value'),
        State('stateExcl', 'value'),
        State('couponMin', 'value'),
        State('couponMax', 'value'),
        # State('price', 'value'),
        # State('yield', 'value'),
        State('maturityMin', 'value'),
        State('maturityMax', 'value'),
        State('call', 'value'),
        State('ratingMin', 'value'),
        State('ratingMax', 'value'),
        # State('accrued', 'value'),
        State('settledate', 'date'),
        # State('sector', 'value'),
        State('manager', 'value')
    ]
)
    
def add_row(n_clicks, data, columns, increment, size, general, stateIncl,
            stateExcl, couponMin, couponMax, maturityMin,
            maturityMax, call, ratingMin, ratingMax, settledate, manager
            ):
    values = [increment, size, general, stateIncl, stateExcl, couponMin, 
            couponMax, maturityMin, maturityMax, call, 
            ratingMin, ratingMax, settledate, manager]
    
    if (n_clicks > 0 and general != '' and increment != '' and size != ''):
        # converts long state to abbrevation for stateIncl/stateExcl
        # values[3] = shorthand[values[3]]
        # values[4] = shorthand[values[4]]

        values[3] = [shorthand[i] for i in values[3]]
        values[4] = [shorthand[i] for i in values[4]]

        # makes string concatentation of multi state
        if len(values[3]) > 1:
            values[3] = ' '.join(values[3])
        if len(values[4]) > 1:
            values[4] = ' '.join(values[4])

        # converts settle date to nice format
        values[12] = datetime.strptime(values[12], '%Y-%m-%dT%H:%M:%S.%f')
        values[12] = datetime.strftime(values[12],'%m/%d/%Y')
        # Dictionary comprehension for adding row to data table
        data.append({
            c['id']:v for c,v in zip(columns, values)
        })
    return data

# Resets/clears template after adding row to data table
# Input: button click
# Output: clears template fields
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
    [Input('editing-rows-button', 'n_clicks')],
    [State('general', 'value'),
    State('increment', 'value'),
    State('size', 'value')
    ]
)
def reset(n_clicks, general, increment, size):
    if (n_clicks > 0 and general != '' and increment != '' and size != ''):
        return '', '', '', '', '', '', '', '', '', '', '', '', datetime.now(), ''
    else:
        raise PreventUpdate


# Data validation for rating min
# Input: rating max
# Output: rating min range based on rating max if specified
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

# Data validation for rating max
# Input: rating min
# Output: rating max range based on rating min if specified
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

# Data validation for maturity min
# Input: maturity max
# Output: maturity min range based on maturity max if specified
@app.callback(
    Output('maturityMin', 'options'),
    [Input('maturityMax', 'value')]
)
def setMaturityMin(year):
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

# Data validation for maturity max
# Input: maturity min
# Output: maturity max range based on maturity min if specified
@app.callback(
    Output('maturityMax', 'options'),
    [Input('maturityMin', 'value')]
)
def setMaturityMax(year):
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

# Data validation for coupon min
# Input: coupon max
# Output: coupon min range based on coupon max if specified
@app.callback(
    Output('couponMin', 'options'),
    [Input('couponMax', 'value')]
)
def setMaturityMin(cpn):
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

# Data validation for coupon max
# Input: coupon min
# Output: coupon max range based on coupon min if specified
@app.callback(
    Output('couponMax', 'options'),
    [Input('couponMin', 'value')]
)
def setMaturityMax(cpn):
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

# Data validation for states to include
# Input: state(s) to exclude
# Output: state(s) that can be included based on state(s) to exclude if specified
@app.callback(
    Output('stateExcl', 'options'),
    [Input('stateIncl', 'value')]
)
def setStateExcl(state):
    if(state == None or state == ''):
        return [
            {'label': s, 'value': s}
            for s in states
        ]
    else:
        return [
            {'label':s, 'value':s}
            for s in states if s not in state
        ]

# Data validation for states to exclude
# Input: state(s) to include
# Output: state(s) that can be excluded based on state(s) to include if specified
@app.callback(
    Output('stateIncl', 'options'),
    [Input('stateExcl', 'value')]
)
def setStateExcl(state):
    if(state == None or state == ''):
        return [
            {'label': s, 'value': s}
            for s in states
        ]
    else:
        return [
            {'label':s, 'value':s}
            for s in states if s not in state
        ]


if __name__ == '__main__':
    app.run_server(debug=False)