#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import six

from .common import ObjectMeta
from ..base import Model
from ..fields import Field, ListField, RequiredField


class ContainerPort(Model):
    name = Field(six.text_type)
    hostPort = Field(int)
    containerPort = Field(int)
    protocol = Field(six.text_type, "TCP")


class ObjectFieldSelector(Model):
    apiVersion = Field(six.text_type)
    fieldPath = RequiredField(six.text_type)


class ResourceFieldSelector(Model):
    containerName = Field(six.text_type)
    resource = RequiredField(six.text_type)
    divisor = Field(six.text_type)


class ConfigMapKeySelector(Model):
    name = Field(six.text_type)
    key = RequiredField(six.text_type)


class SecretKeySelector(Model):
    name = Field(six.text_type)
    key = RequiredField(six.text_type)


class EnvVarSource(Model):
    fieldRef = Field(ObjectFieldSelector)
    resourceFieldRef = Field(ResourceFieldSelector)
    configMapKeyRef = Field(ConfigMapKeySelector)
    secretKeyRef = Field(SecretKeySelector)


class EnvVar(Model):
    name = Field(six.text_type)
    value = Field(six.text_type)
    valueFrom = Field(EnvVarSource)


class ResourceRequirements(Model):
    limits = Field(dict)
    requests = Field(dict)


class VolumeMount(Model):
    name = Field(six.text_type)
    readOnly = Field(bool)
    mountPath = Field(six.text_type)


class HTTPGetAction(Model):
    path = Field(six.text_type)
    port = Field(six.text_type, alt_type=int)
    scheme = Field(six.text_type, "HTTP")
    httpHeaders = Field(list, None)


class HTTPHeader(Model):
    name = Field(six.text_type)
    value = Field(six.text_type)


class TCPSocketAction(Model):
    port = Field(six.text_type, alt_type=int)


class ExecAction(Model):
    command = Field(list)


class Probe(Model):
    httpGet = Field(HTTPGetAction)
    tcpSocket = Field(TCPSocketAction)
    _exec = Field(ExecAction)
    initialDelaySeconds = Field(int, 5)
    timeoutSeconds = Field(int)
    successThreshold = Field(int)
    failureThreshold = Field(int)
    periodSeconds = Field(int)


class Container(Model):
    name = Field(six.text_type)
    image = Field(six.text_type)
    ports = ListField(ContainerPort)
    env = ListField(EnvVar)
    resources = Field(ResourceRequirements)
    volumeMounts = ListField(VolumeMount)
    livenessProbe = Field(Probe)
    readinessProbe = Field(Probe)
    imagePullPolicy = Field(six.text_type, "IfNotPresent")


class SecretVolumeSource(Model):
    secretName = Field(six.text_type)


class KeyToPath(Model):
    key = RequiredField(six.text_type)
    path = RequiredField(six.text_type)


class ConfigMapVolumeSource(Model):
    name = Field(six.text_type)


class EmptyDirVolumeSource(Model):
    medium = Field(six.text_type)


class Volume(Model):
    name = Field(six.text_type)
    secret = Field(SecretVolumeSource)
    configMap = Field(ConfigMapVolumeSource)
    emptyDir = Field(EmptyDirVolumeSource)


class LocalObjectReference(Model):
    name = Field(six.text_type)


class PodSpec(Model):
    volumes = ListField(Volume)
    containers = ListField(Container)
    restartPolicy = Field(six.text_type, "Always")
    terminationGracePeriodSeconds = Field(int)
    activeDeadlineSeconds = Field(int)
    dnsPolicy = Field(six.text_type, "ClusterFirst")
    nodeSelector = Field(dict)
    selector = Field(dict)
    serviceAccountName = Field(six.text_type, "default")
    automountServiceAccountToken = Field(bool)
    imagePullSecrets = ListField(LocalObjectReference)


class PodTemplateSpec(Model):
    metadata = Field(ObjectMeta)
    spec = Field(PodSpec)


class Pod(Model):
    class Meta:
        url_template = "/api/v1/namespaces/{namespace}/pods/{name}"

    metadata = Field(ObjectMeta)
    spec = Field(PodSpec)
