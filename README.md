# [Copernicus Masters 2022](https://copernicus-masters.com/)
# UP42/AirBus
# Sustainable Urban Planning Challenge

## The Challenge
The UP42 Airbus Sustainable Urban Planning Challenge aims to develop algorithms or methodologies that use remote sensing to quantify critical issues emerging from the expansion of historic centres toward modern suburbs.

### Here
Within this repository, we will explore the capabilities of the [UP42 Platform](https://docs.up42.com/), specifically the use of [Python SKD](https://sdk.up42.com/), with which we will obtain the satellite imagery necessary for the analysis that we will show here as an example.

## Our example project
Many of those who make decisions need easy-to-understand data so that they can act on what happens. 
In our case, our example study focuses on inputting information to those who plan about urban areas, who can be Urban Planners, Architects, Engineers and all those who make decisions.
In the following example, we have focused on the old town of [Saint-Malo, France](https://en.wikipedia.org/wiki/Saint-Malo).

We start with a simple question: Are there many cars parked in this area? By being able to answer this question, presenting information over a period of time (time-series), we are able to deliver data to the decision makers and be able to address the problem with other solutions.

[Click here to see the example.](https://github.com/up42/up42-copernicus-masters-2022/blob/master/challenge/CopMa-2022-UP42-Car-Detection.ipynb)
### Custom Block
If you want to use your own data sources or algorithms on the UP42 platform, you can create custom blocks that can be seamlessly added to your workflows as data or processing blocks. These blocks will appear in the console tab Custom blocks.

In simpler words, a custom block is your own data/processing code within the blocks available on the platform.
Your creation can be written in the coding language of your choice, but it is always essential to check the [developers documentation](https://docs.up42.com/developers) in order to make the creation of your block go smoothly.

For more information, please carefully review the list of links below:

|                          Item                                     |               Description                                         |
| :--------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------: |
|                   [Block Manifest](https://docs.up42.com/processing-platform/custom-blocks/manifest)                   |         The JSON-based file format for describing metadata about blocks.          |
|               [Block Capabilities](https://docs.up42.com/processing-platform/custom-blocks/capabilities)               |                  Specifying block input and output capabilities.                  |
|         [Environment Variables](https://docs.up42.com/processing-platform/custom-blocks/environment-variables)         |                  Accessing environment variables inside blocks.                   |
|        [Query Filters & Runtime Parameters](https://docs.up42.com/processing-platform/custom-blocks/parameters)        |  Accepting query filters and runtime parameters for data and processing blocks.   |
|             [Data Transfer Format](https://docs.up42.com/processing-platform/custom-blocks/data-transfer)              |                         Transferring data between blocks.                         |
|                   [GPU Support](https://docs.up42.com/processing-platform/custom-blocks/gpu-support)                   |                     Adding GPU support to processing blocks.                      |
|                  [Storing Data](https://docs.up42.com/processing-platform/custom-blocks/storing-data)                  |                       Storing and accessing data in blocks.                       |
|                  [Publishing Blocks](https://docs.up42.com/processing-platform/custom-blocks/publish)                  |          Publishing data and processing blocks on the UP42 marketplace.           |
|            [Templates & Example Blocks](https://docs.up42.com/processing-platform/custom-blocks/templates)             | Boilerplates and working examples to help you get started with developing blocks. |
|         [Your First Custom Block](https://docs.up42.com/processing-platform/custom-blocks/first-custom-block)          |                      How to upload your first custom block.                       |
| [Developing a Custom Processing Block](https://docs.up42.com/processing-platform/custom-blocks/first-processing-block) |        Walking you through developing your first custom processing block.         |

As an example, we have created 3 Custom Blocks. The examples created correspond to 2 [Data Blocks](https://github.com/up42/up42-copernicus-masters-2022/tree/master/custom_block) to obtain Sentinel-1 images using the [Alaska Satellite Facility (ASF)](https://docs.asf.alaska.edu/api/basics/) and [SentinelSat](https://sentinelsat.readthedocs.io/en/stable/) APIs, and 1 [Processing Block](https://github.com/up42/simple-vegetation-indexes-block) to calculate vegetation indexes for Pléiades, SPOT 6/7 and Sentinel-2.

| **⚠ Disclaimer: The custom blocks created are not official UP42 blocks. They were created for the purpose of providing an example but are not being supported by UP42 for any reason. |
| --- |

### Project ideas:
- The increasing number of structures that have an impact on non-renewable resources (water, vegetation, land).
- The uneven distribution of green sites.
- Wasted spaces to be repurposed as green or residential areas.

We encourage you to consider other use cases that better leverage the most diverse data available on
the UP42 platform.
