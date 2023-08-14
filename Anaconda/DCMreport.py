import os
import shutil
import numpy as np
import pandas as pd
import calendar
import argparse
from datetime import date
from fpdf import FPDF

import matplotlib.pyplot as plt
from matplotlib import rcParams
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

    

# ebonfowl: initiate loop to capture participants from passed participant numbers 'first' to 'last'

# ebonfowl: Load database and grab all needed values to complete document

today = date.today()

# ebonfowl: begin writing PDF

pdf = PDF()

# ebonfowl: Cover Page

pdf.add_page()
pdf.ln(30)
pdf.set_font('Arial', 'B', 20)
pdf.cell(190, 8, 'DCMARVel Testing Report', align = 'C')
# ebonfowl: insert first and last name here
pdf.ln(20)
pdf.set_font('Arial', size=16)
pdf.cell(190, 6, f'Date Generated: {today}', align = 'C')

# ebonfowl: Table of Contents

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'Contents', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)

# ebonfowl: Start neuropsychological assessments

# ebonfowl: ANU-ADRI

pdf.add_page()
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'Thank you for your time, effort, and commitment to participating in this 2 year study! Within this report, you will see the results from your 2 years of testing. The testing analysis includes four time points of measurements including: Baseline, 4-months, 12-months, and 24-months post-baseline testing.', 0)
pdf.ln(10)
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'ANU-ADRI', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'Alzheimer\'s Disease Risk Index (ANU-ADRI): The ANU-ADRI is an evidence-based, validated tool aimed at assessing individual exposure to factors known to be associated with an increased risk of developing Alzheimer\'s Disease and factors which can potentially reduce disease risk.', 0)

# ebonfowl: RBANS

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'RBANS', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'The repeatable battery for the assessment of neurolopsychological status (RBANS) is a brief, individually administered battery to measure neuropsychological cognitive status, and given iteratively over time to assess decline or improvement. The assessment was developed for the dual purposes of identifying and characterizing abnormal cognitive decline in the older adult and as a neuropsychological screening battery for younger patients.\n \nTotal Score Categories:\nOver130: Very Superior\n120-129: Superior\n110-119: High Average\n90-109: Average\n80-89: Low Average\n70-79: Borderline\nBelow 69: Extremely Low', 0)

# ebonfowl: ECOG-12

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'ECOG-12', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'The measurement of Everyday Cognition (ECOG-12) is a very brief assessment consisting of averaging the scores of 12 selected items. The ECog scale covers six domains, everyday memory, language visual-spatial and perceptual abilities, planning, organization, and divided attention.\n \nRatings are made on a four-point scale:\n1 = better or no change compared to 10 years earlier\n2 = questionable/occasionally worse\n3 = consistently a little worse\n4 = consistently much worse', 0)

# ebonfowl: PSQI

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'PSQI', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'The Pittsburgh Sleep Quality Index (PSQI) is a questionnaire that assesses sleep quality and disturbances over a 1-month time interval. Nineteen individual items generate a seven "component" score. Each of the sleep components yields a score randing from 0-3, with 3 indicating the greatest dysfunction. The sleep component scores are summed to yield a total score ranging from 0-21 with the higher total score indicating worse sleep quality.', 0)

# ebonfowl: CES-D

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'CES-D', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'The Center for Epidemiological Studies Depression scale (CES-D) is a 20-item measure that asks participants to rate how often over the past week they experiences symptoms associated with depression such as restless sleep, poor appetite, and feeling lonely. The possible range of scores is 0-60 with the higher scores indicating the presence of moresymptomatology.', 0)

# ebonfowl: GAD-7

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'GAD-7', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'The Generalized Anxiety Disorder Assessment (GAD-7) is a seven-item instrument that is used to measure or assess the severity of generalized anxiety disorder.\n \nScore 0-4: Minimal Anxiety\nScore 5-9: Mild Anxiety\nScore 10-14: Moderate Anxiety\nScore Greater than 15: Severe Anxiety', 0)

# ebonfowl: PSS

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'PSS', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'The Perceived Stress Scale (PSS) is the most widely used psychological instrument for measuring the perception of stress.\n \nScores 0-13: Low Stress\nScores 14-26: Moderate Stress\n27-40 High Perceived Stress', 0)

# ebonfowl: UCLA Loneliness Scale

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'UCLA Loneliness Scale', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'The UCLA Loneliness Scale is designed to measure one\'s subjective feelings of loneliness as well as feelings of social isolation. The scale is scored with a 4-point Likert type scale with possible scores that range from 20-80. Higher scores indicate higher levels of loneliness.', 0)

# ebonfowl: Start anthropometric assessments

# ebonfowl: Height

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'Height', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'Height was measured at each time point. Height is presented here in inches.', 0)

# ebonfowl: Body Mass

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'Body Mass (Weight)', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'Body mass, generally referred to as "weight" in common parlance, was measured at each time point. Body mass is presented here in pounds.', 0)

# ebonfowl: BMI

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'Body Mass Index (BMI)', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)

# ebonfowl: BF%

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'Body Fat Percentage', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)

# ebonfowl: BMD

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'Bone Mineral Density', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)

# ebonfowl: Start pysiological health assessments

# ebonfowl: PHQ-9

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'PHQ-9', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'I don\'t think this one was right.', 0)

# ebonfowl: SF-12

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'SF-12', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'The 12-Item Short Form Health Survey (SF-12) measures general health status in 8 domains (physical functioning, role limitations due to physical problems, bodily pain, general health, vitality, social functioning, role limitations due to emotional problems, and mental health.', 0)

# ebonfowl: Total Cholesterol

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'Total Cholesterol', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'The total amount of cholesterol measured in the bloodstream. Scores below 200mg/dl are generally considered desirabled for total cholesterol, though very high HDL cholesterol can sometimes make total cholesterol appear high even though high HDL cholesterol is indicative of good cholesterol status and cardiovascular disease protection.', 0)

# ebonfowl: LDL Cholesterol

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'LDL Cholesterol', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'Low-density lipoprotein (LDL) cholesterol is generally considered "bad" cholesterol, although some amount is required for proper physiological funcion. Too much LDL cholesterol in your blood may cause the buildup of fatty deposits (plaques) in your arteries (atherosclerosis), which reduces blood flow. These plaques sometimes rupture and can lead to a heart attack or stroke. LDL concentrations below 130 mg/dl are desirable for good health.', 0)

# ebonfowl: HDL Cholesterol

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'HDL Cholesterol', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'High-density lipoprotein (HDL) cholesterol is generally considered "good" cholesterol because it helps carry away LDL cholesterol to be reabsorbed. High levels of HDL cholesterol confer cardiovascular protection and are associated with a reduced risk for cardiovascular disease. HDL concentrations above 40 mg/dl are considered normal, and concentrations above 60 mg/dl are associated with lower cardiovascular disease risk.', 0)

# ebonfowl: Triglycerides

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'Triglycerides', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'Triglycerides refer to fat molecules in the bloodstream. When you eat, your body converts calories it doesn\'t need into triglycerides, which are stored in fat cells. High triglyceride levels are associated with being overweight, eating too many sweets or drinking too much alcohol, smoking, being sedentary, or having diabetes with elevated blood sugar levels. Triglyceride concentrations below 150 mg/dl are considered healthy', 0)

# ebonfowl: Start physical function assessments

# ebonfowl: IPAQ

pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(190, 6, 'IPAQ', align = 'C')
pdf.ln(10)
pdf.set_font('Arial', size=12)
pdf.multi_cell(190, 5, 'International Physical Activity Questionnaire IPAQ: The IPAQ was developed to measure health related physical activity in populations The short version of the IPAQ has been tested extensively and is now used in many international studies.', 0)

# ebonfowl: concatonate strings to form unique pdf name

pdf.output('DCM_Report_Sample.pdf', 'F')