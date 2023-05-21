from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px


app = Flask(__name__)

# import dataset of tv_trp_data
tv_trp_dataset = pd.read_csv('tv_trp_data.csv')
tv_trp_dataset["Viewership"] = pd.to_numeric(tv_trp_dataset["Viewership"].str.replace(" million", ""))

# import dataset of programs_trp_data
programs_trp_dataset = pd.read_csv('programs_trp_data.csv')


# function to generate the TV TRP chart
def generate_tv_trp_chart():
    # create a bar chart
    graph = px.bar(tv_trp_dataset, x='Channel', y='Viewership', color='Day', title='TV TRP',
                   labels={'Viewership': 'Viewership (millions)'})
    graph.update_layout(title_x=0.5)

    # convert the chart to a JSON string
    final_graph = graph.to_json()

    return final_graph


# function to generate the programs chart
def generate_programs_trp_chart(program):
    # creating programs chart of specific program.
    graph = px.line(programs_trp_dataset, x='Minutes', y=program, title='Viewership over time',
                    labels={'Minutes': 'Minutes', 'Viewership': 'Viewership(in millions)'})

    minutes_records_length = len(programs_trp_dataset['Minutes'])
    num_records = minutes_records_length - programs_trp_dataset[program].isna().sum()


    graph.update_xaxes(range=[1, num_records])
    graph.update_layout(title_x=0.5)
    final_graph = graph.to_json()
    return final_graph


# function to get the details of the specific program
def getting_details(program):
    tv_trp_details = tv_trp_dataset[tv_trp_dataset['Program'] == program]
    if not tv_trp_details.empty:
        details = tv_trp_details.iloc[0].to_dict()
        return details
    else:
        return None


# Displaying home web page
@app.route('/')
def home():
    chart = ""
    return render_template('basic_trp.html', chart_safe=chart)


# Displaying page with tv_trp_chart
@app.route('/tv_trp_chart', methods=['POST'])
def overall_trp():
    option = request.form['dropdown']

    if option == 'tv trp':
        final_graph = generate_tv_trp_chart()

    return render_template('basic_trp.html', chart_data=final_graph)


# route to finding more insights page
@app.route('/more_insights', methods=['POST'])
def more_insights():
    chart = ""
    return render_template('program_trp.html', chart_safe=chart)


# displaying the page with program_trp_chart
@app.route('/program_trp_chart', methods=['POST'])
def program_trp():
    option = request.form['dropdown']

    final_graph = generate_programs_trp_chart(option)
    final_details = getting_details(option)

    if final_details is not None:
        channel_txt = final_details['Channel']
        day_txt = final_details['Day']
        time_txt = final_details['Time']
        viewership_txt = final_details['Viewership']
        duration_txt = final_details['Duration (min)']

    return render_template('program_trp.html', chart_data=final_graph, channel_txt=" Channel:{}".format(channel_txt),
                           day_txt="Day:{}".format(day_txt), time_txt="Time:{}".format(time_txt),
                           viewership_txt="Highest viewership recorded(in million):{}".format(viewership_txt),
                           duration_txt="Duration of program(in min):{}".format(duration_txt))


# start of the flask server
if __name__ == '__main__':
    app.run(debug=True)
