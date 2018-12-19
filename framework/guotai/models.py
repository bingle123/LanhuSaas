# -*- coding: utf-8 -*-
from django.db import models


# 国泰君安自动化运维任务模版
class AutoOpsTaskTemplate(models.Model):
    templateName = models.CharField(max_length=100, null=False)
    templateType = models.IntegerField(null=False)
    createTime = models.DateTimeField(null=False)
    createUser = models.CharField(max_length=100, null=False)

    def toDic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


# 国泰君安自动化运维任务
class AutoOpsTask(models.Model):
    taskName = models.CharField(max_length=100, null=False)
    taskPCList = models.TextField(null=False)
    taskType = models.IntegerField(null=False, default=None)
    template = models.ForeignKey(AutoOpsTaskTemplate)
    description = models.CharField(max_length=500, null=False)
    createTime = models.DateTimeField(null=False)
    createUser = models.CharField(max_length=100, null=False)

    def toDic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


# 国泰君安自动化运维任务模版步骤定义
class AutoOpsTaskTemplateStep(models.Model):
    template = models.ForeignKey(AutoOpsTaskTemplate)
    stepName = models.CharField(max_length=100, null=False)
    stepInputParam = models.CharField(max_length=50, null=True)
    stepScriptType = models.IntegerField(null=False)
    stepScriptText = models.TextField(null=False)
    description = models.CharField(max_length=300, null=True)

    def toDic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


# 国泰君安自动化运维任务执行历史
class AutoOpsTaskExecuteHistory(models.Model):
    task = models.ForeignKey(AutoOpsTask)
    state = models.IntegerField(null=False)
    startTime = models.DateTimeField(null=False)
    endTime = models.DateTimeField(null=False)
    actionTime = models.CharField(max_length=50, null=False)
    createUser = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=300, null=True)

    def toDic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


# 国泰君安自动化运维任务执行结果
class AutoOpsTaskResult(models.Model):
    taskHistory = models.ForeignKey(AutoOpsTaskExecuteHistory)
    ip = models.CharField(max_length=100, null=False)
    hostName = models.CharField(max_length=100, null=False)
    actionTime = models.CharField(max_length=50, null=False)
    PassCount = models.IntegerField(null=False)
    NoPassCount = models.IntegerField(null=False)

    def toDic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


# 国泰君安自动化运维任务执行结果详情
class AutoOpsTaskResultDetail(models.Model):
    taskResult = models.ForeignKey(AutoOpsTaskResult)
    name = models.CharField(max_length=100, null=False)
    result = models.CharField(max_length=1000, null=False)

    def toDic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
