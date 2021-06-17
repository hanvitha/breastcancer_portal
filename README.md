# Breast Cancer - Frontend

This is the Flask based frontend app to use [breast cancer detection](https://github.com/hanvitha/breastcancer_detection) model and classify whether the uploaded pathology images are malign or benign.


Before starting off, create a project "ai-ml-demo" in Openshift
```bash
oc new-project ai-ml-demo
```
## Model Deployment in Openshift

### Method 1: Directl deployment using s2i
* From terminal, login to Openshift
* Create a new project using:
```bash
oc new-project ai-ml-demo
```
* Run the below command through terminal:
```bash
oc new-app --name bcd quay.io/hanvithag/model-pipeline-s2i:master~https://github.com/hanvitha/breastcancer_detection.git --build-env S2I_SOURCE_NOTEBOOK_LIST="image_processing_model.ipynb"
```
### Or Using a pipeline
```bash
oc apply -f https://raw.githubusercontent.com/hanvitha/breastcancer_pipelines/master/task/build-source.yaml
oc apply -f https://raw.githubusercontent.com/hanvitha/breastcancer_pipelines/master/resources/build-image.yaml
oc apply -f https://raw.githubusercontent.com/hanvitha/breastcancer_pipelines/master/resources/s2i-model.yaml
oc apply -f https://raw.githubusercontent.com/hanvitha/breastcancer_pipelines/master/pipeline/deploy-pipelines.yaml
```
If you have tekton installed, run 
```bash
tkn pipeline start bcd-pipeline --serviceaccount='pipeline' --showlog
```
Else go to pipeline in Openshift console and Start Run

## Frontend app Installation in Openshift
### From Openshift console:
* Login to Openshift
* Go to Developer perspective
* Make sure you are in bcdemo project
* Click on +Add
* Choose from Git
* Copy paste the current [repo](https://github.com/hanvitha/breastcancer_portal.git) 
* Keep everything default and click Create

### OR from CLI
```bash 
oc new-app https://github.com/hanvitha/breastcancer_portal.git --name bcdemo_ui
oc expose bcdemo_ui
```

## Adding Monitoring and Metrics
### Connecting Prometheus  
```bash
oc new-app prom/prometheus
oc expose service/prometheus

curl https://raw.githubusercontent.com/hanvitha/breastcancer_detection/master/mlworkflows/prometheus.yaml -o prometheus.yaml
oc create configmap prom --from-file=prometheus.yaml
oc set volume deployment/prometheus --add -t configmap --configmap-name=prom -m /etc/prometheus/prometheus.yml --sub-path=prometheus.yaml

oc rollout status -w deployment/prometheus
```
Add sum(pipeline_predictions_total) by (app, value) to monitoring metrics


### Connecting Grafana  
```bash
oc new-app grafana/grafana
oc expose service/grafana
```
Add prometheus dashboard in grafana using:
```bash
http://prometheus.ai-ml-demo:9090
```
Add sum(pipeline_predictions_total) by (app, value) to monitoring metrics and create your own dashboard