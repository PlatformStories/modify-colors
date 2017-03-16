# modify-colors

A GBDX task that modifies the colors of an RGB tif.

## Run

In a Python terminal:

```python
import gbdxtools
from os.path import join
import uuid

gbdx = gbdxtools.Interface()

mf = gbdx.Task('modify-colors')

# Specify input directory
mf.inputs.image = 's3://bucket/prefix/my-directory'

# Specify color pairs separated by semicolons
# The format is color_in_1:color_out_1;color_in_2:color_out_2 etc
mf.inputs.colors = '255,0,0:0,0,255;0,255,0:255,215,0'

# Run gbdx workflow and save results under platform-stories/trial-runs/random_str
wf = gbdx.Workflow([mf])
random_str = str(uuid.uuid4())
output_location = join('platform-stories/trial-runs', random_str)
wf.savedata(mf.outputs.output, output_location)
wf.execute()
```

If there are more than one images in the specified location then only one will be (arbitrarily) picked by the task.


## Input ports

| Name  | Type |  Description | Required |
|-------|--------------|----------------|----------------|
| image | Directory | Contains input tif. | True |
| colors | String | Color pairs. The format is color_in_1:color_out_1;color_in_2:color_out_2 etc. | True |
| transparency | String | Make black pixels transparent. Either 'True' or 'False'. The default is 'False'. | False |

## Output ports

| Name  | Type | Description                  |
|-------|---------|---------------------------|
| output | Directory | Contains output image. |


## Development

### Build the Docker image

You need to install [Docker](https://docs.docker.com/engine/installation/).

Clone the repository:

```bash
git clone https://github.com/digitalglobe/modify-colors
```

Then:

```bash
cd modify-colors
docker build -t modify-colors .
```

### Try out locally

Create a container in interactive mode and mount the sample input under `/mnt/work/input/`:

```bash
docker run -v full/path/to/sample-input:/mnt/work/input -it modify-colors
```

Then, within the container:

```bash
python /modify-colors.py
```

This example changes red to green and green to gold. Confirm that the output image is there
under `/mnt/work/output/output`.

### Docker Hub

Login to Docker Hub:

```bash
docker login
```

Tag your image using your username and push it to DockerHub:

```bash
docker tag modify-colors yourusername/modify-colors
docker push yourusername/modify-colors
```

The image name should be the same as the image name under containerDescriptors in modify-colors.json.

Alternatively, you can link this repository to a [Docker automated build](https://docs.docker.com/docker-hub/builds/).
Every time you push a change to the repository, the Docker image gets automatically updated.

### Register on GBDX

In a Python terminal:

```python
import gbdxtools
gbdx = gbdxtools.Interface()
gbdx.task_registry.register(json_filename='modify-colors.json')
```

Note: If you change the task image, you need to reregister the task with a higher version number
in order for the new image to take effect. Keep this in mind especially if you use Docker automated build.
