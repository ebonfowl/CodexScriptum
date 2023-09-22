import os
import shutil
import numpy as np
import pandas as pd
import calendar
import argparse
from datetime import date
from fpdf import FPDF
from PIL import Image
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from brokenaxes import brokenaxes
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

# create argument parser object
# parser = argparse.ArgumentParser(description='This script returns a report for DCM participants in the given range')

# add positional arguments
# parser.add_argument('first', help = 'The first participant to build a DCM report for', type = int)
# parser.add_argument('last', help = 'The last participant to build a DCM report for', type = int)

# parse arguments
# args = parser.parse_args()

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        
    def header(self):
        # Custom logo and positioning
        self.image('assets/dcm.png', 10, 4, 25)
        # Report title
        # self.set_font('Arial', 'B', 11)
        self.set_font('Arial', size = 11)
        self.cell(self.WIDTH - 80)
        # Page numbers in the header
        self.cell(60, 1, 'DCM Report: Page ' + str(self.page_no()), 0, 0, 'R')
        self.ln(20)
        
    def footer(self):
        # Logos for UArk and NT
        self.image('assets/uark.jpg', 10, 285, 33)
        self.image('assets/nt.jpg', 50, 286, 33)
        # Page numbers in the footer
        # self.set_y(-14)
        # self.set_font('Arial', 'I', 8)
        # self.set_text_color(128)
        # self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'R')

    #def page_body(self, images):
        # Determine how many plots there are per page and set positions
        # and margins accordingly
        #if len(images) == 3:
         #   self.image(images[0], 15, 25, self.WIDTH - 30)
          #  self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
           # self.image(images[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
        #elif len(images) == 2:
         #   self.image(images[0], 15, 25, self.WIDTH - 30)
          #  self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
        #else:
         #   self.image(images[0], 15, 25, self.WIDTH - 30)
            
    #def print_page(self, images):
        # Generates the report
     #   self.add_page()
      #  self.page_body(images)

    def print_page(self):
        self.add_page()

today = date.today() 

# ebonfowl: Load database and grab all needed values to complete document

xls = 'assets/DC MARVEL database.xlsx'

dfMaster = pd.read_excel(xls, 'MASTER DATA').set_index('ID').apply(lambda x: [x if x != '.' else np.NaN for x in x])
dfRBANS = pd.read_excel(xls, 'RBANS').set_index('ID').apply(lambda x: [x if x != '.' else np.NaN for x in x])
dfNT_T1 = pd.read_excel(xls, 'NT_T1').set_index('ID').apply(lambda x: [x if x != '.' else np.NaN for x in x]).apply(pd.to_numeric, errors='coerce')
dfNT_T2 = pd.read_excel(xls, 'NT_T2').set_index('ID').apply(lambda x: [x if x != '.' else np.NaN for x in x]).apply(pd.to_numeric, errors='coerce')
dfNT_T3 = pd.read_excel(xls, 'NT_T3').set_index('ID').apply(lambda x: [x if x != '.' else np.NaN for x in x]).apply(pd.to_numeric, errors='coerce')
dfNT_T4 = pd.read_excel(xls, 'NT_T4').set_index('ID').apply(lambda x: [x if x != '.' else np.NaN for x in x]).apply(pd.to_numeric, errors='coerce')
dfPhysical = pd.read_excel(xls, 'Physical Data').set_index('ID').apply(lambda x: [x if x != '.' else np.NaN for x in x])
dfBridge = pd.read_excel('assets/DCM_Bridge.xlsx').set_index('ID')

# ebonfowl: initiate loop to capture participants from passed participant numbers 'first' to 'last'

i = 179 # ebonfowl: if later integrating argparser, set these equal to the first and last participant arguments
n = 179 # 338

while i <= n:

    dcmID = 'DCM' + str(i)

    # ebonfowl: only make a report for people who actually came at least once

    visits = dfBridge.loc[dcmID]['Visits_Completed']

    if visits != 0:

        # ebonfowl: begin writing PDF, also re-initializes empty class object on each loop iteration

        pdf = PDF()

        # ebonfowl: Cover Page

        firstName = dfBridge.loc[dcmID]['First_Name']
        lastName = dfBridge.loc[dcmID]['Last_Name']

        pdf.add_page()
        pdf.ln(30)
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(190, 8, 'DCMARVel Testing Report', align = 'C')
        pdf.ln(20)
        pdf.cell(190, 8, f'{firstName} {lastName}', align = 'C')
        pdf.ln(20)
        pdf.set_font('Arial', size=16)
        pdf.cell(190, 6, f'Study ID: {dcmID}', align = 'C')
        pdf.ln(10)
        pdf.cell(190, 6, f'Date Generated: {today}', align = 'C')

        # ebonfowl: Table of Contents

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Contents', align = 'C')
        pdf.ln(15)
        pdf.cell(190, 6, 'Cognitive Assessments')
        pdf.ln(8)
        pdf.set_font('Arial', size=12)
        pdf.cell(160, 5, 'ANU-ADRI')
        pdf.cell(30, 5, 'Page 4', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Total Index Score')
        pdf.cell(30, 5, 'Page 5', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Immediate Memory Index')
        pdf.cell(30, 5, 'Page 6', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Visuospatial Index')
        pdf.cell(30, 5, 'Page 7', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Language Index')
        pdf.cell(30, 5, 'Page 8', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Attention Index')
        pdf.cell(30, 5, 'Page 9', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Delayed Memory Index')
        pdf.cell(30, 5, 'Page 10', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: List Learning')
        pdf.cell(30, 5, 'Page 11', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Story Memory')
        pdf.cell(30, 5, 'Page 12', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Figure Copy')
        pdf.cell(30, 5, 'Page 13', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Line Orientation')
        pdf.cell(30, 5, 'Page 14', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Picture Naming')
        pdf.cell(30, 5, 'Page 15', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Semantic Fluency')
        pdf.cell(30, 5, 'Page 16', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Digit Span')
        pdf.cell(30, 5, 'Page 17', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Coding')
        pdf.cell(30, 5, 'Page 18', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: List Recall')
        pdf.cell(30, 5, 'Page 19', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Story Recall')
        pdf.cell(30, 5, 'Page 20', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: List Recognition')
        pdf.cell(30, 5, 'Page 21', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'RBANS: Figure Recall')
        pdf.cell(30, 5, 'Page 22', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Neurotrack: Symbol Match')
        pdf.cell(30, 5, 'Page 23', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Neurotrack: Path Points')
        pdf.cell(30, 5, 'Page 24', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Neurotrack: Item Price')
        pdf.cell(30, 5, 'Page 25', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Neurotrack: Arrow Match')
        pdf.cell(30, 5, 'Page 26', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Neurotrack: Image Pairs')
        pdf.cell(30, 5, 'Page 27', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Neurotrack: Light Reaction')
        pdf.cell(30, 5, 'Page 28', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'ECOG-12')
        pdf.cell(30, 5, 'Page 29', align='R')
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Mental Health Assessments')
        pdf.ln(8)
        pdf.set_font('Arial', size=12)
        pdf.cell(160, 5, 'Pittsburgh Sleep Quality Index (PSQI)')
        pdf.cell(30, 5, 'Page 30', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Center for Epidemiological Studies Depression scale (CES-D)')
        pdf.cell(30, 5, 'Page 31', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Generalized Anxiety Disorder Assessment (GAD-7)')
        pdf.cell(30, 5, 'Page 32', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Perceived Stress Scale (PSS)')
        pdf.cell(30, 5, 'Page 33', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'UCLA Loneliness Scale')
        pdf.cell(30, 5, 'Page 34', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Patient Health Questionaire (PHQ-9)')
        pdf.cell(30, 5, 'Page 35', align='R')
        pdf.ln(6)

        # ebonfowl: Table of Contents page 2
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Contents', align = 'C')
        pdf.ln(15)
        pdf.cell(190, 6, 'Anatomy and Physical Health Assessments')
        pdf.ln(8)
        pdf.set_font('Arial', size=12)
        pdf.cell(160, 5, 'Height')
        pdf.cell(30, 5, 'Page 36', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Body Mass (Weight)')
        pdf.cell(30, 5, 'Page 37', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Body Mass Index (BMI)')
        pdf.cell(30, 5, 'Page 38', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Body Fat Percentage')
        pdf.cell(30, 5, 'Page 39', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Bone Mineral Density')
        pdf.cell(30, 5, 'Page 40', align='R')
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Physiological Health Assessments')
        pdf.ln(8)
        pdf.set_font('Arial', size=12)
        pdf.cell(160, 5, 'Short Form Health Survey (SF-12)')
        pdf.cell(30, 5, 'Page 41', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Total Cholesterol')
        pdf.cell(30, 5, 'Page 42', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'LDL Cholesterol')
        pdf.cell(30, 5, 'Page 43', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'HDL Cholesterol')
        pdf.cell(30, 5, 'Page 44', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Triglycerides')
        pdf.cell(30, 5, 'Page 45', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Blood Glucose')
        pdf.cell(30, 5, 'Page 46', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Resting Heart Rate')
        pdf.cell(30, 5, 'Page 47', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Systolic Blood Pressure')
        pdf.cell(30, 5, 'Page 48', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Diastolic Blood Pressure')
        pdf.cell(30, 5, 'Page 49', align='R')
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Physical Function Assessments')
        pdf.ln(8)
        pdf.set_font('Arial', size=12)
        pdf.cell(160, 5, 'International Physical Activity Questionnaire (IPAQ)')
        pdf.cell(30, 5, 'Page 50', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Short Physical Performance Battery (SPPB)')
        pdf.cell(30, 5, 'Page 51', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, '10-meter Walk')
        pdf.cell(30, 5, 'Page 52', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Handgrip Strength')
        pdf.cell(30, 5, 'Page 53', align='R')
        pdf.ln(6)
        pdf.cell(160, 5, 'Dual-task')
        pdf.cell(30, 5, 'Page 54', align='R')
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(160, 6, 'Credits')
        pdf.set_font('Arial', size=12)
        pdf.cell(30, 6, 'Page 55', align='R')

        # ebonfowl: Start neuropsychological assessments

        # ebonfowl: ANU-ADRI
        sectionName = 'ANU-ADRI'

        pdf.add_page()
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Thank you for your time, effort, and commitment to participating in this 2 year study! Within this report, you will see the results from your 2 years of testing. The testing analysis includes four time points of measurement including: Baseline, 4-months, 12-months, and 24-months post-baseline testing.', 0)
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'ANU-ADRI', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Australia National University Alzheimer\'s Disease Risk Index (ANU-ADRI): The ANU-ADRI is an evidence-based, validated tool aimed at assessing individual exposure to factors known to be associated with an increased risk of developing Alzheimer\'s Disease and factors which can potentially reduce disease risk. A score of zero indicates the average risk for the population. Protective factor score is subtracted from the total, so lower (more negative) scores indicate less risk for Alzheimer\'s disease and higher scores indicate more risk. As the test illustrates risk, not any diagnostic metric, there is no cutoff value other than a score of zero.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['ANUADRI_TOTAL T1']
        yv2 = dfMaster.loc[dcmID]['ANUADRI_TOTAL T2']
        yv3 = dfMaster.loc[dcmID]['ANUADRI_TOTAL T3']
        yv4 = dfMaster.loc[dcmID]['ANUADRI_TOTAL T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = -20
        yt2 = -10
        yt3 = 0
        yt4 = 10
        yt5 = 20
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 0
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4, yt5] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4), str(yt5)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Risk Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS
        sectionName = 'RBANS'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The repeatable battery for the assessment of neurolopsychological status (RBANS) is a brief, individually administered battery to measure neuropsychological cognitive status, and given iteratively over time to assess decline or improvement. The assessment was developed for the dual purposes of identifying and characterizing abnormal cognitive decline in the older adult and as a neuropsychological screening battery for younger patients.\n \nTotal Score Categories:\nOver130: Very Superior\n120-129: Superior\n110-119: High Average\n90-109: Average\n80-89: Low Average\n70-79: Borderline\nBelow 69: Extremely Low', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_ (A) Total Index']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_ (A) Total Index']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_ (A) Total Index']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_ (A) Total Index']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 50
        yt3 = 100
        yt4 = 150
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Total Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Immediate Memory Index
        sectionName = 'RBANS Immediate Memory Index'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Immediate Memory Index', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS immediate memory index indicates a participant\'s ability to learn, and retain presented information when asked to recall that information immediately after presentation. Immediate memory is scored based off the ability to learn a short list of words and a short story, then immediately accurately recall that information to the test administrator. A score of 100 is an average score for immediate memory, and scores below 70 are very low. Lower immediate memory index scores indicate difficulty with verbal learning and memory.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Immediate Memory Index']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Immediate Memory Index']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Immediate Memory Index']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Immediate Memory Index']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 50
        yt3 = 100
        yt4 = 150
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Visuospatial Index
        sectionName = 'RBANS Visuospatial Index'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Visuospatial Index', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Visuospatial Index assesses a participant\'s visual perception, assessment of the spatial relationship of objects, and ability to copy a design from a model. Participants are scored based on ability to copy a figure, and correctly identify the orientation of lines in reference to a fixed object. A score of 100 is an average score for visuospatial index, and scores below 70 are very low. Lower total scores are indicative of difficulty processing and therefore using visual information.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Visuospatial/Constructional Index']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Visuospatial/Constructional Index']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Visuospatial/Constructional Index']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Visuospatial/Constructional Index']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 50
        yt3 = 100
        yt4 = 150
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Language Index
        sectionName = 'RBANS Language Index'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Language Index', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Language Index indicates a participant\'s fluency and ability in expressive language use. The Language Index is scored from ability in naming a pictures of objects and listing examples of a specific semantic category. A score of 100 is an average score for language, and scores below 70 are very low. Lower scores in this index imply difficulties with language, either in learning or remembering language. However, lower scores could also be attributed to deficits when considering fluency versus naming skills or vice versa.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_ Language Index']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_ Language Index']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_ Language Index']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_ Language Index']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 50
        yt3 = 100
        yt4 = 150
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Attention Index
        sectionName = 'RBANS Attention Index'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Attention Index', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Attention Index evaluates a participant\'s ability to remember and manipulate visual and oral information in short-term memory storage. Scoring for attention is based off the ability to accurately repeat strings of numbers and quickly fill numbers corresponding to symbols. A score of 100 is an average score for attention, and scores below 70 are very low. Lower Attention Index scores can indicate low average attentiveness, and either low visual or auditory processing speed.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Attention Index']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Attention Index']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Attention Index']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Attention Index']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 50
        yt3 = 100
        yt4 = 150
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Delayed Memory 
        sectionName = 'RBANS Delayed Memory Index'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Delayed Memory Index', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Delayed Memory Index is similar to the Immediate Memory Index, but measures delayed recall and recognition for verbal and visual information. Delayed memory tests the participant\'s ability, after completing several other tasks, to recall a list of words, choose these words from a list, recall a story, and draw a figure from memory. A score of 100 is an average score for delayed memory, and scores below 70 are very low. Lower scores in these assesments indicate difficulty in recognizing or retrieving long-term memory. Since this index contains both visual and auditory tests, difficulties with sight or hearing can also impact the total score.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Delayed Memory Index']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Delayed Memory Index']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Delayed Memory Index']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Delayed Memory Index']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 50
        yt3 = 100
        yt4 = 150
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS List Learning
        sectionName = 'RBANS List Learning'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS List Learning', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS List Learning subtest assesses a participant\'s ability to learn a list of words, and measures habitual verbal memory function. A list of 10 words is read to the participant, who is then responsible for repeating back as many words as they remember, in any order. This process is repeated a total of 4 times. For each word the participant correctly recalls, 1 point is earned. Scores for this assessment range from 0 to 40. Lower scores indicate a difficulty learning new verbal information, and that repitition may not significantly improve learning ability for that individual. There are no established reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_List Learning_raw score']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_List Learning_raw score']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_List Learning_raw score']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_List Learning_raw score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 15
        yt3 = 30
        yt4 = 40
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Story Memory
        sectionName = 'RBANS Story Memory'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Story Memory', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Story Memory subtest tests a participant\'s ability to memorize conceptually related verbal information in the form of a short story. A short story is read to the participant, who repeats back as much of the story as they remember. The process is repeated once more, with the participant earning 1 point for each keyword repeated verbatim. Story memory scores range from 0 to 24. Lower scores indicate difficulty learning new verbal information, and that repitition may not significantly improve learning ability. There are no established reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Story Memory_raw score']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Story Memory_raw score']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Story Memory_raw score']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Story Memory_raw score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 8
        yt3 = 16
        yt4 = 24
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Figure Copy
        sectionName = 'RBANS Figure Copy'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Figure Copy', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Figure Copy subtest assesses a participant\'s ability to copy a complex geometric design. This requires the participant to utilize several cognitive skills including: visuospatial reasoning, attention to visual details, motor programming, organization, and fine motor skills. Each portion of the participant\'s drawing is scored for correctness and completeness. Total score for the figure copy ranges from 0 to 20. Lower scores in this assessment can be related to difficulties with sight, perceiving spatial or visual relationships, or fine motor skill issues. There are no established reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Figure Copy_raw score']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Figure Copy_raw score']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Figure Copy_raw score']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Figure Copy_raw score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 6
        yt3 = 13
        yt4 = 20
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Line Orientation
        sectionName = 'RBANS Line Orientation'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Line Orientation', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Line Orientation subtest measures a participant\'s ability to correctly determine spatial orientation of lines in two-dimensional space. In a diagram, 13 lines are spaced equally over 180 degrees. 2 additional lines are then presented, both relating to a line from the diagram. 1 point is earned for each line the participant correctly identifies, for a total score ranging from 0 to 20. Lower scores on this subtest indicate difficulty in processing visual relationships between objects, or general visual impairment. There are no established reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Line Orientation_raw score']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Line Orientation_raw score']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Line Orientation_raw score']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Line Orientation_raw score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 6
        yt3 = 13
        yt4 = 20
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Picture Naming
        sectionName = 'RBANS Picture Naming'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Picture Naming', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Picture Naming subtest tests a participant\'s ability to use confrontation naming skills when presented with simple drawings of common objects. A participant is presented with 10 drawings total, one at a time, and asked to name it. For each drawing that is properly named, the participant earns 1 point. The total score of this subtest ranges from 0 to 10. Low scores indicate significant difficulty in object recognition. There are no established reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Picture Naming_raw score']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Picture Naming_raw score']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Picture Naming_raw score']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Picture Naming_raw score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 3
        yt3 = 7
        yt4 = 10
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Semantic Fluency
        sectionName = 'RBANS Semantic Fluency'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Semantic Fluency', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Semantic Fluency subtest assesses a participant\'s ability to retrieve and express words using a semantic prompt (list the names of animals, musical instruments, articles of clothing, etc.). For each word the participant says that follows the given prompt, 1 point is awarded. Total score for semantic fluency ranges from 0 to 40. Lower scores indicate difficulty in remembering and expressing words from long-term memory storage. There are no established reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Sementic Fluency_raw score']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Sementic Fluency_raw score']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Sementic Fluency_raw score']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Sementic Fluency_raw score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 15
        yt3 = 30
        yt4 = 40
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Digit Span
        sectionName = 'RBANS Digit Span'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Digit Span', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Digit Span subtest measures a participant\'s auditory registration and brief focused attention. A string of numbers is read to the participant, who is responsible for repeating the string of numbers back, as accurately as possible. For each string correctly repeated on the first try, the participant earns 2 points, or 1 point if correct on the second try. Total score for digit span ranges from 0 to 16. Lower scores indicate difficulty with auditory attention and registration. There are no established reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Digit Span_raw score']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Digit Span_raw score']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Digit Span_raw score']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Digit Span_raw score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 5
        yt3 = 10
        yt4 = 16
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Coding
        sectionName = 'RBANS Coding'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Coding', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Coding subtest assesses a participant\'s brief and focused visual attention, visual scanning, and processing speed. Participant\'s must quickly fill in blanks with numbers that correspond to various symbols. For each number that correctly corresponds to a symbol, 1 point is earned. Total score in coding ranges from 0 to 89. Lower scores in this subtest indicate difficulties with processing speed and brief, focused attention to visual detail. There are no established reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Coding_raw score']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Coding_raw score']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Coding_raw score']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Coding_raw score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 30
        yt3 = 60
        yt4 = 90
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS List Recall
        sectionName = 'RBANS List Recall'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS List Recall', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS List Recall subtest measures a participant\'s free recall ability of unrelated words. This subtest is directly related to list learning. List recall tests long term memory, utilizing a long break between learning the list and recalling it. Participants are asked to recall the list of words read at the beginning of the RBANS assessment. For every word correctly recalled, 1 point is earned. Total score ranges from 0 to 10. Lower scores in this subtest indicate difficulty with long term memory retention and retrieving verbal information. There are no established reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_List Recall_raw score']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_List Recall_raw score']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_List Recall_raw score']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_List Recall_raw score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 3
        yt3 = 7
        yt4 = 10
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Story Recall
        sectionName = 'RBANS Story Recall'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Story Recall', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Story Recall subtest measures delayed free recall of related verbal information. This subtest directly relates to story memory. Story recall tests long term memory, utilizing a long break between learning the story and recalling it. The participant is asked to recall the story read at the beginning of the RBANS assesment. For each keyword repeated verbatim, 1 point is earned. Total score for story recall ranges from 0 to 12. If the story recall score is significantly lower than story memory, it indicates poor memory or forgetfulness. If story recall and story memory are both low, this indicates difficulty learning and recalling conceptually related verbal information. Low scores in story recall indicate difficulty retrieving verbal information. There are no established reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Story Recall_raw score']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Story Recall_raw score']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Story Recall_raw score']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Story Recall_raw score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 4
        yt3 = 8
        yt4 = 12
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS List Recognition
        sectionName = 'RBANS List Recognition'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS List Recognition', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS List Recognition subtest assesses a participant\'s delayed recognition memory. This subtest directly relates to both list learning and recall, as the participant must recognize the list of words from a larger list of words. A new list of words, containing the original list and additional words, is read to the participant one by one. For each word correctly identified as in the original list or not, 1 point is earned. Total score for list recognition ranges from 0 to 20. If list recognition score is significantly lower than list recall, it indicates the participant has difficulty receiving verbal information. If list recognition and list recall are similarly low in score, this indicates general difficulty learning and remembering verbal information. Low scores in list recognition indicate a difficulty recognizing verbal information, and that repitition may not help with learning verbal information. There are no established reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_List Recognition_raw score']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_List Recognition_raw score']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_List Recognition_raw score']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_List Recognition_raw score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 6
        yt3 = 13
        yt4 = 20
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: RBANS Figure Recall
        sectionName = 'RBANS Figure Recall'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'RBANS Figure Recall', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The RBANS Figure Recall subtest measures a participant\'s delayed free recall ability of conceptually related visuospatial and detail information. This subtest is directly related to figure copy. Participants are asked to recall, and draw from memory, the figure they copied at the beginning of the RBANS assessment. For every part and location correctly drawn, 1 point is earned. Total score for figure recall ranges from 0 to 20. If figure recall is significantly lower than figure copy, this indicates difficulty with long term visual relation and detail memory. If the figure recall and copy scores are similarly low, it indicates difficulty receiving visual information instead. Low scores in just figure recall indicate difficulty recalling these visuospatial and detail information. There are no established reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfRBANS.loc[dcmID]['RBANS_Trial1_Figure Recall_raw score']
        yv2 = dfRBANS.loc[dcmID]['RBANS_Trial2_Figure Recall_raw score']
        yv3 = dfRBANS.loc[dcmID]['RBANS_Trial3_Figure Recall_raw score']
        yv4 = dfRBANS.loc[dcmID]['RBANS_Trial4_Figure Recall_raw score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 6
        yt3 = 13
        yt4 = 20
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Symbol Match
        sectionName = 'Symbol Match'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Neurotrack: Symbol Match', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Symbol Match is a processing speed and executive functioning task that utilizes a paired verification or rejection paradigm (forced choice). Participants are instructed to determine whether two symbols are equal or unequal utilizing a legend with nine number/symbol pairs. Symbol Match is based on the traditional Digit Symbol Substitution test. Primary scores are based on accuracy and speed. Higher scores represent more correct trials completed within the allotted time limit and higher processing speed. Low processing speed may indicate problems with quick decision making. There are no validated reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfNT_T1.loc[i]['NT Processing Speed_Time point 1_Raw Score']
        yv2 = dfNT_T2.loc[i]['NT Processing Speed_Time point 2_Raw Score']
        yv3 = dfNT_T3.loc[i]['NT Processing Speed_Time point 3_Raw Score']
        yv4 = dfNT_T4.loc[i]['NT Processing Speed_Time point 4_Raw Score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 16
        yt3 = 33
        yt4 = 50
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Path Points
        sectionName = 'Path Points'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Neurotrack: Path Points', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The Path Points assessment is a measure of executive function and attention that requires participants to connect a set of circles by alternating between numbers and letters (e.g. 1-A-2-B-3-C...). The task is a digitized version of the Trail Making Test Part B. The primary assessment score is based on completion time with lower scores indicating better test performance and better executive function. Impaired executive function may lead to difficuty with decision making. There are no validated reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfNT_T1.loc[i]['NT Executive Function_Time point 1_Raw Score'] * -1
        yv2 = dfNT_T2.loc[i]['NT Executive Function_Time point 2_Raw Score'] * -1
        yv3 = dfNT_T3.loc[i]['NT Executive Function_Time point 3_Raw Score'] * -1
        yv4 = dfNT_T4.loc[i]['NT Executive Function_Time point 4_Raw Score'] * -1
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 13
        yt3 = 27
        yt4 = 40
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Time to Complete (sec)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Item Price
        sectionName = 'Item Price'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Neurotrack: Item Price', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Item Price is a brief visual paired associates paradigm that measures visual recognition memory and episodic memory. This task requires participants to learn a series of food/price pairs and discriminate between target and foil pairs during a recognition trial. All items belong to the same semantic category (fruits, vegetables, etc.) and are presented in random order. Primary scores are based on accuracy and higher scores indicate more correct responses and better associative learning ability. Low associative learning ability may indicate a reduced ability to commit associations to memory such as the scheduled time of events, the location of objects, and the prices of goods and services. There are no validated reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfNT_T1.loc[i]['NT Associative Learning_Time point 1_Raw Score'] * 100
        yv2 = dfNT_T2.loc[i]['NT Associative Learning_Time point 2_Raw Score'] * 100
        yv3 = dfNT_T3.loc[i]['NT Associative Learning_Time point 3_Raw Score'] * 100
        yv4 = dfNT_T4.loc[i]['NT Associative Learning_Time point 4_Raw Score'] * 100
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 33
        yt3 = 67
        yt4 = 100
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Percent Correct")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Arrow Match
        sectionName = 'Arrow Match'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Neurotrack: Arrow Match', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The Arrow Match assessment is a measure of attention and processing speed. Participants are shown an arrow on one side of the screen and tasked with identifying which direction the arrow is pointing. The arrows can point in either the same direction as the side of the screen (e.g. an arrow on the right side of the screen points right) or in the opposite direction from the side of the screen it is displayed on (e.g. an arrow on the right side of the screen points left). Primary scores are based on the rate of getting trials correct (# of correct responses/total time elapsed) with higher scores indicating better attention. Low attention may indicate an individual\'s inability to remain focused and attentive during tasks. There are no validated reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfNT_T1.loc[i]['NT Attention_Time point 1_Raw Score']
        yv2 = dfNT_T2.loc[i]['NT Attention_Time point 2_Raw Score']
        yv3 = dfNT_T3.loc[i]['NT Attention_Time point 3_Raw Score']
        yv4 = dfNT_T4.loc[i]['NT Attention_Time point 4_Raw Score']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = .66
        yt3 = 1.34
        yt4 = 2
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Correct Score Rate (sec)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Image Pairs
        sectionName = 'Image Pairs'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Neurotrack: Image Pairs', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The Image Pairs assessment is a measure of associative and recognition memory. Participants are presented with a series of target images and are asked to identify the same target images (familiar) when paired with novel images (unfamiliar). The task is repeated using the now familiar pairs in which the participant is asked to discriminate between familiar and unfamiliar pairs. Primary scores are based on accuracy (percent correct) and consist of novelty preference and behavioral response metrics. Score represents a participant\'s ability to remember associations and low scores may indicate a problem with remembering associations after they are learned. There are no validated reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfNT_T1.loc[i]['NT Associative Memory_Time point 1_Raw Score'] * 100
        yv2 = dfNT_T2.loc[i]['NT Associative Memory_Time point 2_Raw Score'] * 100
        yv3 = dfNT_T3.loc[i]['NT Associative Memory_Time point 3_Raw Score'] * 100
        yv4 = dfNT_T4.loc[i]['NT Associative Memory_Time point 4_Raw Score'] * 100
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 33
        yt3 = 67
        yt4 = 100
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Percent Correct")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Light Reaction
        sectionName = 'Light Reaction'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Neurotrack: Light Reaction', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The Light Reaction assessment is a measure of attention and inhibitory control. Participants are presented with either a positive stimulus (green light) or negative stimulus (red light). If the positive stimulus appears, they are tasked with pressing a button. If the negative stimulus appears, they are tasked with refraining from pressing the button. Speed and accuracy are both measured, with both errors of omission (failing to press the button when appropriate) and errors of commission (pressing the button when not appropriate) quantified. The primary assessment score is based on accuracy and speed (average response time for correct responses) and low scores may indicate impaired decision inhibition. There are no validated reference ranges for this individual assessment, but results are included to illustrate change over time.', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfNT_T1.loc[i]['NT-Inhibition_Time point 1_Raw Score'] * -1 / 1000
        yv2 = dfNT_T2.loc[i]['NT-Inhibition_Time point 2_Raw Score'] * -1 / 1000
        yv3 = dfNT_T3.loc[i]['NT-Inhibition_Time point 3_Raw Score'] * -1 / 1000
        yv4 = dfNT_T4.loc[i]['NT-Inhibition_Time point 4_Raw Score'] * -1 / 1000
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = .33
        yt3 = .67
        yt4 = 1
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 70
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Average Response Time (sec)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: ECOG-12
        sectionName = 'ECOG-12'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'ECOG-12', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The measurement of Everyday Cognition (ECOG-12) is a very brief assessment consisting of averaging the scores of 12 selected items. The ECog scale covers six domains, everyday memory, language visual-spatial and perceptual abilities, planning, organization, and divided attention.\n \nRatings are made on a four-point scale:\n1 = better or no change compared to 10 years earlier\n2 = questionable/occasionally worse\n3 = consistently a little worse\n4 = consistently much worse', 0)
        pdf.image('assets/cognitive_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['ECOG-12 T1']/12
        yv2 = dfMaster.loc[dcmID]['ECOG-12 T2']/12
        yv3 = dfMaster.loc[dcmID]['ECOG-12 T3']/12
        yv4 = dfMaster.loc[dcmID]['ECOG-12 T4']/12
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 1.3
        yt3 = 2.7
        yt4 = 4
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 3
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: PSQI
        sectionName = 'PSQI'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'PSQI', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The Pittsburgh Sleep Quality Index (PSQI) is a questionnaire that assesses sleep quality and disturbances over a 1-month time interval. Nineteen individual items generate a seven "component" score. Each of the sleep components yields a score randing from 0-3, with 3 indicating the greatest dysfunction. The sleep component scores are summed to yield a total score ranging from 0-21 with the higher total score indicating worse sleep quality. A score grater than 5 indicates poor sleep which can impact energy levels and mental accuity throughout the day, and is associated with many negative health outcomes such as obesity, cognitive disease, and heart disease.', 0)
        pdf.image('assets/mental_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['PSQI_Sleep T1']
        yv2 = dfMaster.loc[dcmID]['PSQI_Sleep T2']
        yv3 = dfMaster.loc[dcmID]['PSQI_Sleep T3']
        yv4 = dfMaster.loc[dcmID]['PSQI_Sleep T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 7
        yt3 = 14
        yt4 = 21
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 5
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: CES-D
        sectionName = 'CES-D'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'CES-D', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The Center for Epidemiological Studies Depression scale (CES-D) is a 20-item measure that asks participants to rate how often over the past week they experiences symptoms associated with depression such as restless sleep, poor appetite, and feeling lonely. The possible range of scores is 0-60 with the higher scores indicating the presence of more symptomatology which is associated with higher cognitive disease risk and lower subjective quality of life. Scores over 16 indicate significant depressive symptomology.\n \n*Note. All results should be verified by a clinician for a definitive diagnosis and treatment options.', 0)
        pdf.image('assets/mental_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['CES-D T1']
        yv2 = dfMaster.loc[dcmID]['CES-D T2']
        yv3 = dfMaster.loc[dcmID]['CES-D T3']
        yv4 = dfMaster.loc[dcmID]['CES-D T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 20
        yt3 = 40
        yt4 = 60
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 16
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: GAD-7
        sectionName = 'GAD-7'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'GAD-7', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The Generalized Anxiety Disorder Assessment (GAD-7) is a seven-item instrument that is used to assess the severity of generalized anxiety disorder. High levels of anxiety can lead to gastrointestinal issues and increase the risk of cardiovascular disease, diabetes, and all-cause mortality.\n \nScore 0-4: Minimal Anxiety\nScore 5-9: Mild Anxiety\nScore 10-14: Moderate Anxiety\nScore Greater than 15: Severe Anxiety\n \n*Note. All results should be verified by a clinician for a definitive diagnosis and treatment options.', 0)
        pdf.image('assets/mental_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['GAD-7 T1']
        yv2 = dfMaster.loc[dcmID]['GAD-7 T2']
        yv3 = dfMaster.loc[dcmID]['GAD-7 T3']
        yv4 = dfMaster.loc[dcmID]['GAD-7 T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 7
        yt3 = 14
        yt4 = 20
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 15
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: PSS
        sectionName = 'PSS'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'PSS', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The Perceived Stress Scale (PSS) is the most widely used psychological instrument for measuring the perception of stress. High levels of stress are associated with obesity, cardiovasular disease, decreased subjective quality of life, and cognitive disease, as well as many other negative health states.\n \nScores 0-13: Low Stress\nScores 14-26: Moderate Stress\n27-40: High Perceived Stress\n \n*Note. All results should be verified by a clinician for a definitive diagnosis and treatment options.', 0)
        pdf.image('assets/mental_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['Perceived Stress T1']
        yv2 = dfMaster.loc[dcmID]['Perceived Stress T2']
        yv3 = dfMaster.loc[dcmID]['Perceived Stress T3']
        yv4 = dfMaster.loc[dcmID]['Perceived Stress T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 13
        yt3 = 27
        yt4 = 40
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 27
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: UCLA Loneliness Scale
        sectionName = 'UCLA Loneliness Scale'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'UCLA Loneliness Scale', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The UCLA Loneliness Scale (3-item) is designed to measure one\'s subjective feelings of loneliness as well as feelings of social isolation. The scale is scored with a 4-point Likert type scale with possible scores that range from 0-9. Higher scores indicate higher levels of loneliness which is associated with cognitive disease, lower subjective quality of life, and negative emotion. A score greater than 6 indicates significant loneliness.\n \n*Note. All results should be verified by a clinician for a definitive diagnosis and treatment options.', 0)
        pdf.image('assets/mental_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['UCLA Loneliness T1']
        yv2 = dfMaster.loc[dcmID]['UCLA Loneliness T2']
        yv3 = dfMaster.loc[dcmID]['UCLA Loneliness T3']
        yv4 = dfMaster.loc[dcmID]['UCLA Loneliness T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 3
        yt3 = 6
        yt4 = 9
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 6
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: PHQ-9
        sectionName = 'PHQ-9'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'PHQ-9', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'PHQ-9 is an assessment of depression.  This self-report tool is used as a screening only and is not indicative of a depression diagnosis. Higher scores indicate greater levels of depression which is associated with cognitive disease, decreased subjective quality of life, and many other negative health states.\n \nScore Categories:\n1-4: Minimal Depression\n5-9: Mild Depression\n10-14: Moderate Depression\n15-19: Moderately Severe Depression\n20-27: Severe Depression\n \n*Note. All results should be verified by a clinician for a definitive diagnosis and treatment options.', 0)
        pdf.image('assets/mental_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['PHQ-9 T1']
        yv2 = dfMaster.loc[dcmID]['PHQ-9 T2']
        yv3 = dfMaster.loc[dcmID]['PHQ-9 T3']
        yv4 = dfMaster.loc[dcmID]['PHQ-9 T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 7
        yt3 = 14
        yt4 = 27
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 15
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Start anthropometric assessments

        # ebonfowl: Height
        sectionName = 'Height'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Height', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Height was measured at each time point. Height is presented here in inches.', 0)
        pdf.image('assets/physical_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfPhysical.loc[i]['Height (cm)_1']/2.54
        yv2 = dfPhysical.loc[i]['Height (cm)_2']/2.54
        yv3 = dfPhysical.loc[i]['Height (cm)_3']/2.54
        yv4 = dfPhysical.loc[i]['Height (cm)_4']/2.54
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 50
        yt2 = 59
        yt3 = 68
        yt4 = 77
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 15
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Height (in)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Body Mass
        sectionName = 'Body Mass'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Body Mass (Weight)', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Body mass, generally referred to as "weight" in common parlance, was measured at each time point. Body mass is presented here in pounds.', 0)
        pdf.image('assets/physical_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfPhysical.loc[i]['Weight (kg)_1'] * 2.2
        yv2 = dfPhysical.loc[i]['Weight (kg)_2'] * 2.2
        yv3 = dfPhysical.loc[i]['Weight (kg)_3'] * 2.2
        yv4 = dfPhysical.loc[i]['Weight (kg)_4'] * 2.2
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 100
        yt2 = 180
        yt3 = 260
        yt4 = 340
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 15
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Body Mass (lbs.)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: BMI
        sectionName = 'Body Mass Index'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Body Mass Index (BMI)', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'BMI is used as a measurement to estimate body fat and is calculated as body mass (in kilograms) divided by the square of height (in meters). It is commonly used in clinical settings to predict risk for health issues such as heart disease, high blood pressure, and type 2 diabetes.\n \n<18.5: Underweight\n18.5-24.9: Normal\n25.0-29.9: Overweight\n30.0-34.9: Obese, Class 1\n35.0-39.9: Obese, Class 2\n>40: Obese, Class 3\n \n*Note. BMI is never used to diagnose the presence of any disease. It is used to assess risk.', 0)
        pdf.image('assets/physical_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['BMI_T1']
        yv2 = dfMaster.loc[dcmID]['BMI_T2']
        yv3 = dfMaster.loc[dcmID]['BMI_T3']
        yv4 = dfMaster.loc[dcmID]['BMI_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 18
        yt2 = 27
        yt3 = 36
        yt4 = 46
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 30
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Body Mass Index (kg/m^2)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: BF%
        sectionName = 'Body Fat Percentage'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Body Fat Percentage', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Body fat percentage is a percentage of how much of your body mass is fat compared to the rest of the make-up of your body such as muscles, bones, and organs. Knowing your %BF can give you more detailed information of you body composition and potentially, cardiovascular health risk those with higher percentages of body fat tend to be at higher risk for cardiovascular disease. Currently, there are no universal norms what your %BF should be, however, it is believed that females should aim to have a %BF <31%, and males should aim to have a %BF <21%.', 0)
        pdf.image('assets/physical_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['BFP_T1']
        yv2 = dfMaster.loc[dcmID]['BFP_T2']
        yv3 = dfMaster.loc[dcmID]['BFP_T3']
        yv4 = dfMaster.loc[dcmID]['BFP_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 12
        yt2 = 28
        yt3 = 44
        yt4 = 60
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        sex = dfMaster.loc[dcmID]['Sex']
        if sex == 'M':
            cutoff = 21
            Go = True
        elif sex == 'F':
            cutoff = 31
            Go = True
        else:
            Go = False
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        if Go == True:
            plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Body Fat Percentage")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: BMD
        sectionName = 'Bone Mineral Density'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Bone Mineral Density', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'BMD is a measurement of the calcium and other minerals in bones. Bones higher in minerals are denser, tend to be stronger, and less likely to break. Some diseases and aging can cause bones to become less dense, increasing the risk for fractures and broken bones. Assessments of BMD will result in a T-score which is how the assessment is interpreted.\n \nT-score of -1 or higher: Healthy bone\nT-score of -1 to -2.5: Osteopenia\nT-score of -2.5 or lower: Osteoporosis', 0)
        pdf.image('assets/physical_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfPhysical.loc[i]['TotZScr_1']
        yv2 = dfPhysical.loc[i]['TotZScr_2']
        yv3 = dfPhysical.loc[i]['TotZScr_3']
        yv4 = dfPhysical.loc[i]['TotTScr_4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = -4
        yt2 = -1
        yt3 = 0
        yt4 = 4
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = -2.5
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("T-Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Start pysiological health assessments

        # ebonfowl: SF-12
        sectionName = 'SF-12'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'SF-12', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The 12-Item Short Form Health Survey (SF-12) measures general health status in 8 domains (physical functioning, role limitations due to physical problems, bodily pain, general health, vitality, social functioning, role limitations due to emotional problems, and mental health). Scores are given on a 0 to 100 scale with higher scores indicating a better overall health state. There is no established cutoff score for the overall SF-12, so your scores are presented here to illustrate change over time.', 0)
        pdf.image('assets/physiological_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['SF-12_Health T1']
        yv2 = dfMaster.loc[dcmID]['SF-12_Health T2']
        yv3 = dfMaster.loc[dcmID]['SF-12_Health T3']
        yv4 = dfMaster.loc[dcmID]['SF-12_Health T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 33
        yt3 = 67
        yt4 = 100
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 6
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Total Cholesterol
        sectionName = 'Total Cholesterol'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Total Cholesterol', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The total amount of cholesterol measured in the bloodstream. Scores below 200mg/dl are generally considered desirabled for total cholesterol, though very high HDL cholesterol can sometimes make total cholesterol appear high even though high HDL cholesterol is indicative of good cholesterol status and cardiovascular disease protection. High cholesterol can be indicative of cardiovascular disease risk, though examining LDL and HDL cholesterol values independently can be more informative', 0)
        pdf.image('assets/physiological_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['TC_T1']
        yv2 = dfMaster.loc[dcmID]['TC_T2']
        yv3 = dfMaster.loc[dcmID]['TC_T3']
        yv4 = dfMaster.loc[dcmID]['TC_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 100
        yt2 = 150
        yt3 = 200
        yt4 = 300
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 200
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Blood Cholesterol (mg/dl)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: LDL Cholesterol
        sectionName = 'LDL Cholesterol'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'LDL Cholesterol', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Low-density lipoprotein (LDL) cholesterol is generally considered "bad" cholesterol, although some amount is required for proper physiological funcion. Too much LDL cholesterol in your blood may cause the buildup of fatty deposits (plaques) in your arteries (atherosclerosis), which reduces blood flow. These plaques sometimes rupture and can lead to a heart attack or stroke. LDL concentrations below 130 mg/dl are desirable for good health.', 0)
        pdf.image('assets/physiological_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['LDL_T1']
        yv2 = dfMaster.loc[dcmID]['LDL_T2']
        yv3 = dfMaster.loc[dcmID]['LDL_T3']
        yv4 = dfMaster.loc[dcmID]['LDL_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 20
        yt2 = 75
        yt3 = 130
        yt4 = 200
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 130
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Blood Cholesterol (mg/dl)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: HDL Cholesterol
        sectionName = 'HDL Cholesterol'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'HDL Cholesterol', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'High-density lipoprotein (HDL) cholesterol is generally considered "good" cholesterol because it helps carry away LDL cholesterol to be reabsorbed. High levels of HDL cholesterol confer cardiovascular protection and are associated with a reduced risk for cardiovascular disease. HDL concentrations above 40 mg/dl are considered normal, and concentrations above 60 mg/dl are associated with lower cardiovascular disease risk.', 0)
        pdf.image('assets/physiological_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['HDL_T1']
        yv2 = dfMaster.loc[dcmID]['HDL_T2']
        yv3 = dfMaster.loc[dcmID]['HDL_T3']
        yv4 = dfMaster.loc[dcmID]['HDL_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 40
        yt3 = 60
        yt4 = 100
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 40
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Blood Cholesterol (mg/dl)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Triglycerides
        sectionName = 'Triglycerides'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Triglycerides', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Triglycerides refer to fat molecules in the bloodstream. When you eat, your body converts calories it doesn\'t need into triglycerides, which are stored in fat cells. High triglyceride levels are associated with being overweight, eating too many sweets or drinking too much alcohol, smoking, being sedentary, or having diabetes with elevated blood sugar levels. Triglyceride concentrations below 150 mg/dl are considered healthy', 0)
        pdf.image('assets/physiological_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['TRG_T1']
        yv2 = dfMaster.loc[dcmID]['TRG_T2']
        yv3 = dfMaster.loc[dcmID]['TRG_T3']
        yv4 = dfMaster.loc[dcmID]['TRG_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 150
        yt3 = 300
        yt4 = 400
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 150
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Blood Triglycerides (mg/dl)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Blood Glucose
        sectionName = 'Blood Glucose'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Blood Glucose', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Blood glucose is the measure of sugar in the blood.  This test is used to determine an individual\'s risk of developing diabetes and blood glucose control for individuals with a diabetes diagnosis.\n \nCategories:\n70-100 mg/dL: Normal fasting blood glucose\n100-125 mg/dL: Prediabetes\n>126* mg/dL: Diabetes\n \n*Note. You may not have had a true fasting blood glucose measurement.  Fasting means you did not have anything to eat or drink other than water or black coffee at least 8 hours before your test.  Also, if your values are over 126 mg/dL they must be confirmed by a clinician before a diagnosis is made.', 0)
        pdf.image('assets/physiological_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['GLU_T1']
        yv2 = dfMaster.loc[dcmID]['GLU_T2']
        yv3 = dfMaster.loc[dcmID]['GLU_T3']
        yv4 = dfMaster.loc[dcmID]['GLU_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 60
        yt2 = 100
        yt3 = 125
        yt4 = 250
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 100
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Blood Glucose (mg/dl)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Resting Heart Rate
        sectionName = 'Resting Heart Rate'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Resting Heart Rate', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Resting Heart Rate (RHR) is the number of times your heart is beating each minute. There are a lot of factors that can cause your heart rate to increase including stimulants such as caffeine and stress. Additionally, there are factors that cause your heart rate to decrease such as an increase in cardiovascular fitness. 60-100 bpm is considered the normal range for RHR. An elevated resting heart rate can be indicative of poor cardiovascular health or cardiovascular disease risk, though it is a relatively poor indicator compared to blood pressure and blood lipid profile.', 0)
        pdf.image('assets/physiological_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['HR_T1']
        yv2 = dfMaster.loc[dcmID]['HR_T2']
        yv3 = dfMaster.loc[dcmID]['HR_T3']
        yv4 = dfMaster.loc[dcmID]['HR_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 30
        yt2 = 60
        yt3 = 100
        yt4 = 150
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 100
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Heart Rate (beats/min)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Systolic Blood Pressure
        sectionName = 'Systolic Blood Pressure'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Systolic Blood Pressure', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Systolic Blood Pressure is the top number of your blood pressure reading. This is a measure of the pressure of the blood in your arteries when your heart beats. High systolic blood pressure can lead to stroke, heart disease, and chronic kidney disease.\n \n<120 mmHg: Normal\n120-129 mmHg: Elevated\n130-139 mmHg: Stage 1 Hypertension\n>140 mmHg: Stage 2 Hypertension\n \n*Note. Hypertension (high blood pressure) must be diagnosed by a clinician on more than one occasion.', 0)
        pdf.image('assets/physiological_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['SBP_T1']
        yv2 = dfMaster.loc[dcmID]['SBP_T2']
        yv3 = dfMaster.loc[dcmID]['SBP_T3']
        yv4 = dfMaster.loc[dcmID]['SBP_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 80
        yt2 = 100
        yt3 = 130
        yt4 = 200
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 130
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Blood Pressure (mmHg)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Diastolic Blood Pressure
        sectionName = 'Diastolic Blood Pressure'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Diastolic Blood Pressure', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Diastolic Blood Pressure is the bottom number of your blood pressure reading. This is a measure of the pressure of the blood in your arteries between heart beats.\n \n<80 mmHg: Normal\n80-89 mmHg: Stage 1 Hypertension\n>90 mmHg: Stage 2 Hypertension\n \n*Note. Hypertension (high blood pressure) must be diagnosed by a clinician on more than one occasion.', 0)
        pdf.image('assets/physiological_health_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['DBP_T1']
        yv2 = dfMaster.loc[dcmID]['DBP_T2']
        yv3 = dfMaster.loc[dcmID]['DBP_T3']
        yv4 = dfMaster.loc[dcmID]['DBP_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 50
        yt2 = 80
        yt3 = 100
        yt4 = 120
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 80
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Blood Pressure (mmHg)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Start physical function assessments

        # ebonfowl: IPAQ
        sectionName = 'IPAQ'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'IPAQ', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'International Physical Activity Questionnaire IPAQ: The IPAQ was developed to measure health related physical activity. The short version of the IPAQ has been tested extensively and is now used in many international studies. Based on the amount of physical activity performed in the last week, a participant is determined to either have a high, medium, or low level of physical activity. Low physical activity and sedentary behavior has been linked to nearly every physiological and metabolic negative health states including cardiovascular disease, cancer, cognitive disease and diabetes', 0)
        pdf.image('assets/physical_function_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['IPAQ T1']
        if yv1 == 'LOW':
            yv1 = 1
        elif yv1 == 'MODERATE':
            yv1 = 2
        elif yv1 == 'HIGH':
            yv1 = 3
        yv2 = dfMaster.loc[dcmID]['IPAQ T2']
        if yv2 == 'LOW':
            yv2 = 1
        elif yv2 == 'MODERATE':
            yv2 = 2
        elif yv2 == 'HIGH':
            yv2 = 3
        yv3 = dfMaster.loc[dcmID]['IPAQ T3']
        if yv3 == 'LOW':
            yv3 = 1
        elif yv3 == 'MODERATE':
            yv3 = 2
        elif yv3 == 'HIGH':
            yv3 = 3
        yv4 = dfMaster.loc[dcmID]['IPAQ T4']
        if yv4 == 'LOW':
            yv4 = 1
        elif yv4 == 'MODERATE':
            yv4 = 2
        elif yv4 == 'HIGH':
            yv4 = 3
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 1
        yt3 = 2
        yt4 = 3
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 1
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = ['', 'Low', 'Moderate', 'High']
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Physical Activity Level")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: SPPB
        sectionName = 'SPPB'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'SPPB', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The Short Physical Performance Battery (SPPB) is an objective assessment tool for evaluating lower extremity function and mobility in older persons. The assessment is made up of 3 tests: walking, sit-to-stand, and balance. The scoring ranges from zero (worst performance) to 12 points (best performance).\n \nScore Classifications:\n0-4: disability/very poor performance \n4-6: poor performance\n7-9: moderate performance\n10-12: good performance', 0)
        pdf.image('assets/physical_function_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['SPPB_T1']
        yv2 = dfMaster.loc[dcmID]['SPPB_T2']
        yv3 = dfMaster.loc[dcmID]['SPPB_T3']
        yv4 = dfMaster.loc[dcmID]['SPPB_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = 4
        yt3 = 8
        yt4 = 12
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 4
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Score")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: 10-meter Walk
        sectionName = '10-meter Walk'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, '10-meter Walk', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The 10-m walk test is an assessment that measures walking speed over a short distance. It is a tool to determine functional mobility, gait, and vestibular function. Impaired walking speed can limit the ability of an individual to complete everyday activities effectively, such as crossing the street while the "walk" sign is illuminated.\n \nNormative Values (Average walking speed by age group)\n40-49: 1.43-1.39 m/s\n50-59: 1.43-1.31 m/s\n60-69: 1.34-1.24 m/s\n70-79: 1.26-1.13 m/s', 0)
        pdf.image('assets/physical_function_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = 10/dfMaster.loc[dcmID]['10mWalk_T1']
        yv2 = 10/dfMaster.loc[dcmID]['10mWalk_T2']
        yv3 = 10/dfMaster.loc[dcmID]['10mWalk_T3']
        yv4 = 10/dfMaster.loc[dcmID]['10mWalk_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 0
        yt2 = .8
        yt3 = 1.6
        yt4 = 2.4
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 1.2
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Walking Speed (m/sec)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Handgrip Strength
        sectionName = 'Handgrip Strength'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Handgrip Strength', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'The handgrip assessment measures muscular strength and is used as a screening tool for upper body strength and overall strength. The participant squeezes a handle as hard as they can and it measures the maximal isometric force produced during the squeeze. Low levels of strength can lead to impaired functional ability, especially as individuals age. The threshold value (orange line) on the graph below is placed based on your age and sex, a total handgrip force below this line indicates "poor" grip strength.', 0)
        pdf.image('assets/physical_function_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['Grip_T1'] * 4.4
        yv2 = dfMaster.loc[dcmID]['Grip_T2'] * 4.4
        yv3 = dfMaster.loc[dcmID]['Grip_T3'] * 4.4
        yv4 = dfMaster.loc[dcmID]['Grip_T4'] * 4.4
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = 50
        yt2 = 150
        yt3 = 250
        yt4 = 350
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        sex = dfMaster.loc[dcmID]['Sex']
        age = dfMaster.loc[dcmID]['Age']
        if sex == 'M':
            Go = True
            if age >= 60:
                cutoff = 159
            elif age >= 50:
                cutoff = 166
            elif age >= 40:
                cutoff = 175
            else:
                Go = False
        elif sex == 'F':
            Go = True
            if age >= 60:
                cutoff = 89
            elif age >= 50:
                cutoff = 98
            elif age >= 40:
                cutoff = 106
            else:
                Go = False
        else:
            Go = False
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        if Go == True:
            plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Handfrip Force (lbs.)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: Dual Task
        sectionName = 'Dual Task'

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Dual Task', align = 'C')
        pdf.ln(10)
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(190, 5, 'Dual-task walking is an assessment that measures attention and executive function by performing an attention-demanding task during a walking trial. Walking 10-meters and counting backwards by three starting from a random 3-digit number is the assessment that we utilized in this study. The percent slowdown that occurs from walking without counting to the dual-task walking trials is called dual-task cost (DTC). Lower (more negative) DTC indicates a participant struggles with performing physical and mental tasks simultaneously. There are currently no accepted normative values for DTC, your data are presented here to demonstrate change over time.', 0)
        pdf.image('assets/physical_function_banner.png', 112, 284, 90)

        ###### Y VALUES AT EACH TIMEPOINT ######
        yv1 = dfMaster.loc[dcmID]['DTC_T1']
        yv2 = dfMaster.loc[dcmID]['DTC_T2']
        yv3 = dfMaster.loc[dcmID]['DTC_T3']
        yv4 = dfMaster.loc[dcmID]['DTC_T4']
        ###### END Y VALUES ######
        
        ###### GRAPH Y-TICK SPACING ######
        yt1 = -120
        yt2 = -60
        yt3 = 0
        yt4 = 30
        ###### END Y-TICK SPACING ######

        ###### CUTOFF VALUE ######
        cutoff = 1.2
        ###### CUTOFF VALUE ######

        x = np.array([1, 4, 12, 24]) # x values
        y = np.array([yv1, yv2, yv3, yv4])
        x_ticks = [0, 4, 12, 24]
        x_labels = ['0', '4', '12', '24']

        y_ticks = [yt1, yt2, yt3, yt4] 
        y_labels = [str(yt1), str(yt2), str(yt3), str(yt4)]
        
        # first plot with X and Y data
        fig = plt.plot(x, y, marker='o')
        
        x1 = [1, 4, 12, 24] # x values
        y1 = [cutoff, cutoff, cutoff, cutoff] # y values to create a cutoff point
        
        # second plot for line depicting cutoff value
        # plt.plot(x1, y1, '-.')
        
        plt.xlabel("Months")
        plt.ylabel("Dual-Task Cost (% Change)")
        plt.xticks(ticks=x_ticks, labels=x_labels)
        plt.yticks(ticks=y_ticks, labels=y_labels)
        plt.title(sectionName)
        graphName = 'assets/graphs/DCM'+str(i)+'_'+sectionName+'_graph.png'
        plt.savefig(graphName, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()

        pdf.image(graphName, 20, 135, 150)
        pdf.image('assets/uark.jpg', 10, 285, 33)
        pdf.image('assets/nt.jpg', 50, 286, 33)

        # ebonfowl: credits page

        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 6, 'Credits', align = 'C')
        pdf.ln(10)
        pdf.cell(90, 5, 'University of Arkansas Team:')
        pdf.cell(40, 5, '')
        pdf.cell(60, 5, 'Neurotrack Team:')
        pdf.ln(8)
        pdf.set_font('Arial', size=12)
        pdf.cell(90, 5, 'Dr. Michelle Gray')
        pdf.cell(40, 5, '')
        pdf.cell(60, 5, 'Dr. Jordan Glenn')
        pdf.ln(6)
        pdf.cell(90, 5, 'Dr. Sally Paulson')
        pdf.cell(40, 5, '')
        pdf.cell(60, 5, 'Dr. Kelsey Bryk')
        pdf.ln(6)
        pdf.cell(90, 5, 'Dr. Cody Diehl')
        pdf.cell(40, 5, '')
        pdf.cell(60, 5, 'Natalie Justice')
        pdf.ln(6)
        pdf.cell(90, 5, 'Dr. Josh Gills')
        pdf.cell(40, 5, '')
        pdf.cell(60, 5, 'Erica Madero')
        pdf.ln(6)
        pdf.cell(90, 5, 'Anthony Campitelli')
        pdf.cell(40, 5, '')
        pdf.cell(60, 5, 'Dr. Jennifer Myer')
        pdf.ln(6)
        pdf.cell(90, 5, 'Megan Jones')
        pdf.cell(40, 5, '')
        pdf.cell(60, 5, '')
        pdf.ln(6)
        pdf.cell(90, 5, 'Ray Urbina')
        pdf.cell(40, 5, '')
        pdf.cell(60, 5, '')
        pdf.ln(20)
        pdf.multi_cell(190, 5, 'The whole DC MARVel team would like to thank you for your participation in this study! Two years is a major commitment of your time and energy. It is only because of our amazing participants that we are able to conduct our important research, and we sincerely appreciate you. We will be in touch regarding future research opportunities you may qualify for but, for now, we wish you well and look forward to seeing you again! Woo pig!', 0)
        pdf.image('assets/Duckling.jpg', 50, 161, 90)
        pdf.ln(138)
        pdf.multi_cell(190, 5, f'This report was generated on {today} with software written by Anthony Campitelli', 0)

        # ebonfowl: concatonate strings to form unique pdf name

        reportname = 'dcmReports/DCM'+str(i)+'_Post-Study_Report.pdf'

        pdf.output(reportname, 'F')

    i = i + 1